from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import torch.nn as nn

from transformers.models.llama.modeling_llama import LlamaForCausalLM, LlamaModel

from typing import Optional, Tuple, Union, List
from transformers.cache_utils import Cache, DynamicCache
from transformers.modeling_outputs import (
    BaseModelOutputWithPast,
    CausalLMOutputWithPast
)
from transformers.utils import (
    logging
)
#from .configuration_llama import LlamaConfig

logger = logging.get_logger(__name__)

import psutil
import time


class LlamaForCrossAttention(LlamaForCausalLM):
    def __init__(self, causal_llama, cross_attention_frequency=1):
        
        # Copy every attr from the original model, except that the model gets converted to a cross attention model
        for key, value in causal_llama.__dict__.items():
            setattr(self, key, value)
        
        self.model = XLlamaModel(causal_llama.model, cross_attention_frequency)
    
    #@add_start_docstrings_to_model_forward(LLAMA_INPUTS_DOCSTRING)
    #@replace_return_docstrings(output_type=CausalLMOutputWithPast, config_class=_CONFIG_FOR_DOC)
    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        labels: Optional[torch.LongTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        # the new thing we're adding
        cross_key_values: Optional[torch.FloatTensor] = None,
    ) -> Union[Tuple, CausalLMOutputWithPast]:
        r"""
        Args:
            labels (`torch.LongTensor` of shape `(batch_size, sequence_length)`, *optional*):
                Labels for computing the masked language modeling loss. Indices should either be in `[0, ...,
                config.vocab_size]` or -100 (see `input_ids` docstring). Tokens with indices set to `-100` are ignored
                (masked), the loss is only computed for the tokens with labels in `[0, ..., config.vocab_size]`.

        Returns:

        Example:

        ```python
        >>> from transformers import AutoTokenizer, LlamaForCausalLM

        >>> model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-hf")
        >>> tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

        >>> prompt = "Hey, are you conscious? Can you talk to me?"
        >>> inputs = tokenizer(prompt, return_tensors="pt")

        >>> # Generate
        >>> generate_ids = model.generate(inputs.input_ids, max_length=30)
        >>> tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        "Hey, are you conscious? Can you talk to me?\nI'm not conscious, but I can talk to you."
        ```"""
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        # decoder outputs consists of (dec_features, layer_state, dec_hidden, dec_attn)
        outputs = self.model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            inputs_embeds=inputs_embeds,
            use_cache=use_cache,
            output_attentions=output_attentions,
            output_hidden_states=output_hidden_states,
            return_dict=return_dict,
            cache_position=cache_position,
            cross_key_values=cross_key_values
        )

        hidden_states = outputs[0]
        if self.config.pretraining_tp > 1:
            lm_head_slices = self.lm_head.weight.split(self.vocab_size // self.config.pretraining_tp, dim=0)
            logits = [F.linear(hidden_states, lm_head_slices[i]) for i in range(self.config.pretraining_tp)]
            logits = torch.cat(logits, dim=-1)
        else:
            logits = self.lm_head(hidden_states)
        logits = logits.float()

        loss = None
        if labels is not None:
            # Shift so that tokens < n predict n
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()
            # Flatten the tokens
            loss_fct = CrossEntropyLoss()
            shift_logits = shift_logits.view(-1, self.config.vocab_size)
            shift_labels = shift_labels.view(-1)
            # Enable model parallelism
            shift_labels = shift_labels.to(shift_logits.device)
            loss = loss_fct(shift_logits, shift_labels)

        if not return_dict:
            output = (logits,) + outputs[1:]
            return (loss,) + output if loss is not None else output

        return CausalLMOutputWithPast(
            loss=loss,
            logits=logits,
            past_key_values=outputs.past_key_values,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )

    def prepare_inputs_for_generation(
        self,
        input_ids,
        past_key_values=None,
        attention_mask=None,
        inputs_embeds=None,
        cache_position=None,
        use_cache=True,
        cross_key_values=None,
        **kwargs,
    ):
        # Call this method using the parent class, which knows how to handle everything except for cross_key_values
        model_inputs = super().prepare_inputs_for_generation(
            input_ids=input_ids,
            past_key_values=past_key_values,
            attention_mask=attention_mask,
            inputs_embeds=inputs_embeds,
            cache_position=cache_position,
            use_cache=use_cache,
            **kwargs,
        )

        # Add the cross_key_values to the model inputs
        model_inputs["cross_key_values"] = cross_key_values

        return model_inputs
    


class CrossAttentionLayer(nn.Module):
    def __init__(self, dim, n_heads, parent_model):
        super().__init__()
        # make sure it has the same device/float type as the rest of the model 
        #self.q_proj = nn.Linear(dim, dim, bias=False, device=parent_model.device, dtype=parent_model.dtype)
        #self.n_heads = n_heads
        self.xattention = nn.MultiheadAttention(dim, n_heads, device=parent_model.device, dtype=parent_model.dtype, batch_first=True)
    
    def forward(self, x, context):
        if context is None: return x
        output, _ = self.xattention(x, context, context)
        return x + output

class XLlamaModel(LlamaModel):
    """
    [Cross Attention +] Transformer decoder consisting of *config.num_hidden_layers* layers. Each layer is a [`LlamaDecoderLayer`]

    Args:
        config: LlamaConfig
    """

    def __init__(self, original_model: LlamaModel, cross_attention_frequency=1):
        # Copy every attr from the original model
        for key, value in original_model.__dict__.items():
            setattr(self, key, value)
        # add cross attention layers
        self.x_layers = nn.ModuleList([CrossAttentionLayer(self.config.hidden_size, self.config.num_attention_heads, parent_model=original_model)
                                       for _ in range(self.config.num_hidden_layers//cross_attention_frequency)])
        self.cross_attention_frequency = cross_attention_frequency

    def forward(
        self,
        input_ids: torch.LongTensor = None,
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[Union[Cache, List[torch.FloatTensor]]] = None,
        inputs_embeds: Optional[torch.FloatTensor] = None,
        use_cache: Optional[bool] = None,
        output_attentions: Optional[bool] = None,
        output_hidden_states: Optional[bool] = None,
        return_dict: Optional[bool] = None,
        cache_position: Optional[torch.LongTensor] = None,
        # this is what's been added: cross attention inputs
        cross_key_values: Optional[torch.FloatTensor] = None
    ) -> Union[Tuple, BaseModelOutputWithPast]:
        
        if cross_key_values is None:
            print("WARNING: no cross-attention target provided in xllama.forward")
        
        output_attentions = output_attentions if output_attentions is not None else self.config.output_attentions
        output_hidden_states = (
            output_hidden_states if output_hidden_states is not None else self.config.output_hidden_states
        )
        use_cache = use_cache if use_cache is not None else self.config.use_cache
        return_dict = return_dict if return_dict is not None else self.config.use_return_dict

        if (input_ids is None) ^ (inputs_embeds is not None):
            raise ValueError(
                "You cannot specify both input_ids and inputs_embeds at the same time, and must specify either one"
            )

        if self.gradient_checkpointing and self.training and use_cache:
            logger.warning_once(
                "`use_cache=True` is incompatible with gradient checkpointing. Setting `use_cache=False`."
            )
            use_cache = False

        if inputs_embeds is None:
            inputs_embeds = self.embed_tokens(input_ids)

        return_legacy_cache = False
        if use_cache and not isinstance(past_key_values, Cache):  # kept for BC (non `Cache` `past_key_values` inputs)
            return_legacy_cache = True
            past_key_values = DynamicCache.from_legacy_cache(past_key_values)
            logger.warning_once(
                "We detected that you are passing `past_key_values` as a tuple and this is deprecated and will be removed in v4.43. "
                "Please use an appropriate `Cache` class (https://huggingface.co/docs/transformers/v4.41.3/en/internal/generation_utils#transformers.Cache)"
            )

        if cache_position is None:
            past_seen_tokens = past_key_values.get_seq_length() if past_key_values is not None else 0
            cache_position = torch.arange(
                past_seen_tokens, past_seen_tokens + inputs_embeds.shape[1], device=inputs_embeds.device
            )
        if position_ids is None:
            position_ids = cache_position.unsqueeze(0)

        causal_mask = self._update_causal_mask(
            attention_mask, inputs_embeds, cache_position, past_key_values, output_attentions
        )

        # embed positions
        hidden_states = inputs_embeds

        # decoder layers
        all_hidden_states = () if output_hidden_states else None
        all_self_attns = () if output_attentions else None
        next_decoder_cache = None

        for layer_index, decoder_layer in enumerate(self.layers):
            if output_hidden_states:
                all_hidden_states += (hidden_states,)

            if self.gradient_checkpointing and self.training:
                layer_outputs = self._gradient_checkpointing_func(
                    decoder_layer.__call__,
                    hidden_states,
                    causal_mask,
                    position_ids,
                    past_key_values,
                    output_attentions,
                    use_cache,
                    cache_position,
                )
            else:
                layer_outputs = decoder_layer(
                    hidden_states,
                    attention_mask=causal_mask,
                    position_ids=position_ids,
                    past_key_value=past_key_values,
                    output_attentions=output_attentions,
                    use_cache=use_cache,
                    cache_position=cache_position,
                )

            hidden_states = layer_outputs[0]

            if use_cache:
                next_decoder_cache = layer_outputs[2 if output_attentions else 1]

            if output_attentions:
                all_self_attns += (layer_outputs[1],)
            
            # cross attention
            if layer_index % self.cross_attention_frequency == 0:
                hidden_states = self.x_layers[layer_index//self.cross_attention_frequency](hidden_states, cross_key_values)

        hidden_states = self.norm(hidden_states)

        # add hidden states from the last decoder layer
        if output_hidden_states:
            all_hidden_states += (hidden_states,)

        next_cache = next_decoder_cache if use_cache else None
        if return_legacy_cache:
            next_cache = next_cache.to_legacy_cache()

        if not return_dict:
            return tuple(v for v in [hidden_states, next_cache, all_hidden_states, all_self_attns] if v is not None)
        return BaseModelOutputWithPast(
            last_hidden_state=hidden_states,
            past_key_values=next_cache,
            hidden_states=all_hidden_states,
            attentions=all_self_attns,
        )


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description = "")
    parser.add_argument("--max_tokens", type=int, default=2048, help="max number of tokens for generation")
    parser.add_argument("--temperature", "-t", type=float, default=0.5)
    parser.add_argument("--xa", type=int, default=0, help="how many cross attention tokens to try")
    parser.add_argument("--xa_frequency", type=int, default=1, help="how often to do cross attention")
    parser.add_argument("--batch_size", "-b", type=int, default=1, help="how many samples to draw")
    arguments = parser.parse_args()

    model_id = "codellama/CodeLlama-7b-hf"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype=torch.float16
    )
    try:
        model.to("cuda")
        print("moved model to gpu")
    except Exception as e:
        print("could not move model to gpu", e)
    
        
    print("about to create cross attention model, memory usage:", psutil.Process().memory_info().rss / 1024 ** 2 / 1024 ** 2, "GB")
    print("model parameters:", len(list(model.parameters())))
    xmodel = LlamaForCrossAttention(model, cross_attention_frequency=arguments.xa_frequency)    
    print("cross attention model parameters:", len(list(xmodel.parameters())))
    #import pdb; pdb.set_trace()
    model = xmodel
    
    print("created cross attention model, memory usage:", psutil.Process().memory_info().rss / 1024 ** 2 / 1024 ** 2, "GB")

    print("about to do rollout, memory usage:", psutil.Process().memory_info().rss / 1024 ** 2 / 1024 ** 2, "GB")
    # Generate from the model, using the prefix "def fibonacci("
    prompt = "def fibonacci("
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
    # cross attention data
    if arguments.xa > 0:
        cross_key_values = torch.randn(1, arguments.xa, 1024*4, device=model.device, dtype=model.dtype)
    else:
        cross_key_values = None
    
    start_time = time.time()
    output = model.generate(input_ids, max_length=arguments.max_tokens, num_return_sequences=arguments.batch_size, temperature=arguments.temperature, cross_key_values=cross_key_values)
    end_time = time.time()
                            
    print(tokenizer.decode(output[0], skip_special_tokens=True))
    print("total time(s):", end_time - start_time)
    print("tokens/sec:", arguments.max_tokens * arguments.batch_size / (end_time - start_time))