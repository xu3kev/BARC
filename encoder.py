import math
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import pytorch_lightning as pl

from arc import train_problems, validation_problems

def positional_encoding_2d(xs, ys, hidden_dim):
    assert xs.size(0) == ys.size(0)
    assert xs.size(1) == ys.size(1)

    position_encodings = torch.zeros(xs.size(0), xs.size(1), hidden_dim)
    position_encodings = position_encodings.to(xs.device)
    position_encodings.requires_grad = False

    # first wave has a period of 2
    # second wave has 3
    # ...
    periods = torch.arange(2, hidden_dim//4 + 2)

    xs, ys = xs+1, ys+1
    position_encodings[:, :, 0::4] = torch.sin(2*math.pi* xs.unsqueeze(-1) / periods.unsqueeze(0).unsqueeze(0))
    position_encodings[:, :, 1::4] = torch.cos(2*math.pi* xs.unsqueeze(-1) / periods.unsqueeze(0).unsqueeze(0))
    position_encodings[:, :, 2::4] = torch.sin(2*math.pi* ys.unsqueeze(-1) / periods.unsqueeze(0).unsqueeze(0))
    position_encodings[:, :, 3::4] = torch.cos(2*math.pi* ys.unsqueeze(-1) / periods.unsqueeze(0).unsqueeze(0))

    return position_encodings

# Define the Transformer Encoder
class ARCEncoder(nn.Module):
    def __init__(self, hidden_dim, num_layers, num_heads, max_examples=6):
        super(ARCEncoder, self).__init__()
        self.color_embedding = nn.Embedding(10+1, hidden_dim)
        self.example_embedding = nn.Embedding(max_examples, hidden_dim)
        self.input_output_imbedding = nn.Embedding(2, hidden_dim)
        self.transformer_layers = nn.ModuleList([
            nn.TransformerEncoderLayer(hidden_dim, num_heads, batch_first=False)
            for _ in range(num_layers)
        ])
        
        self.hidden_dim = hidden_dim
        self.mask_index = 10 # this color counts as mask
        self.num_heads = num_heads

    def forward(self, colors, xs, ys, es, io, sequence_lengths=None):
        color_embedded = self.color_embedding(colors)
        example_embedded = self.example_embedding(es)
        position_embedded = positional_encoding_2d(xs, ys, self.hidden_dim)
        io_embedded = self.input_output_imbedding(io)

        embedded = color_embedded + example_embedded + position_embedded + io_embedded

        if sequence_lengths is not None:
            #construct src_mask, src_key_padding_mask
            src_mask = torch.zeros(embedded.size(0)*self.num_heads, embedded.size(1), embedded.size(1), dtype=torch.bool)
            src_key_padding_mask = torch.zeros(embedded.size(0), embedded.size(1), dtype=torch.bool)
            for i, l in enumerate(sequence_lengths):
                src_mask[i*self.num_heads : (i+1)*self.num_heads, l:, :] = True
                src_mask[i*self.num_heads : (i+1)*self.num_heads, :, l:] = True
                src_key_padding_mask[i, l:] = True
            # replicate for each head
            src_mask = src_mask.to(embedded.device)
            src_key_padding_mask = src_key_padding_mask.to(embedded.device)
        else:
            src_mask = None
            src_key_padding_mask = None

        embedded = embedded.permute(1, 0, 2)
        for layer in self.transformer_layers:
            embedded = layer(embedded, src_key_padding_mask=src_key_padding_mask)#, src_mask=src_mask)
        return embedded.permute(1, 0, 2)

def test_encoder():
    # Create a sample input and test that masking works correctly
    hidden_dim = 256
    num_layers = 16
    num_heads = 8
    max_examples = 5
    model = TransformerEncoder(hidden_dim, num_layers, num_heads, max_examples)
    batch_size = 4
    sequence_length = 32
    colors = torch.randint(0, 10, (batch_size, sequence_length))
    xs = torch.randint(0, 10, (batch_size, sequence_length))
    ys = torch.randint(0, 10, (batch_size, sequence_length))
    es = torch.randint(0, max_examples, (batch_size, sequence_length))
    ios = torch.randint(0, 2, (batch_size, sequence_length))
    sequence_lengths = torch.randint(1, sequence_length, (batch_size,))

    model.eval()

    out = model(colors, xs, ys, es, ios, sequence_lengths)
    for i, l in enumerate(sequence_lengths):
        these_colors = colors[i, :l].unsqueeze(0)
        these_xs = xs[i, :l].unsqueeze(0)
        these_ys = ys[i, :l].unsqueeze(0)
        these_es = es[i, :l].unsqueeze(0)
        these_ios = ios[i, :l].unsqueeze(0)
        these_sequence_lengths = sequence_lengths[i].unsqueeze(0)
        these_out = model(these_colors, these_xs, these_ys, these_es, these_ios, None)
        print(out[i, :l])
        print(these_out.squeeze(0)[:l])
        tolerance = 1e-5
        assert torch.allclose(out[i, :l], these_out.squeeze(0), atol=tolerance), f"differed by at most {torch.max(torch.abs(out[i, :l] - these_out.squeeze(0)))}"
        
# how to use ARC  data to produce the things needed for encoder:
def tokenize_problem(problem):
    if not isinstance(problem, list):
        problem = problem.train_pairs + problem.test_pairs
    xs, ys, ios, es, colors = [], [], [], [], []
    for example_index, train_pair in enumerate(problem):
        # these are numpy arrays
        if hasattr(train_pair, 'x'):
            input_grid = train_pair.x
            output_grid = train_pair.y
        elif isinstance(train_pair, tuple):
            input_grid = train_pair[0]
            output_grid = train_pair[1]

        for x in range(input_grid.shape[0]):
            for y in range(input_grid.shape[1]):
                xs.append(x)
                ys.append(y)
                ios.append(0)
                es.append(example_index)
                colors.append(input_grid[x, y])
        for x in range(output_grid.shape[0]):
            for y in range(output_grid.shape[1]):
                xs.append(x)
                ys.append(y)
                ios.append(1)
                es.append(example_index)
                colors.append(output_grid[x, y])
    return torch.tensor(xs), torch.tensor(ys), torch.tensor(ios), torch.tensor(es), torch.tensor(colors)


class ARCDataset(Dataset):
    def __init__(self, problems):
        self.problems = problems
    def __len__(self):
        return len(self.problems)
    def __getitem__(self, idx):
        return tokenize_problem(self.problems[idx])

def collate_fn(batch):
    # batch is a list of samples, each of which is a tuple of tensors
    lengths = [len(x[0]) for x in batch]
    # everyone needs to be padded with 0s to the max length
    max_length = max(lengths)
    for i in range(len(batch)):
        xs, ys, ios, es, colors = batch[i]
        padding = max_length - len(xs)
        batch[i] = (torch.cat([xs, torch.zeros(padding, dtype=torch.long)]),
                    torch.cat([ys, torch.zeros(padding, dtype=torch.long)]),
                    torch.cat([ios, torch.zeros(padding, dtype=torch.long)]),
                    torch.cat([es, torch.zeros(padding, dtype=torch.long)]),
                    torch.cat([colors, torch.zeros(padding, dtype=torch.long)]))
    
    batched_xs = torch.stack([x[0] for x in batch])
    batched_ys = torch.stack([x[1] for x in batch])
    batched_ios = torch.stack([x[2] for x in batch])
    batched_es = torch.stack([x[3] for x in batch])
    batched_colors = torch.stack([x[4] for x in batch])
    return batched_xs, batched_ys, batched_ios, batched_es, batched_colors, torch.tensor(lengths)

# define data loaders
train_dataset = ARCDataset(train_problems)
train_loader = DataLoader(train_dataset, batch_size=3, shuffle=True, collate_fn=collate_fn)
validation_dataset = ARCDataset(validation_problems)
validation_loader = DataLoader(validation_dataset, batch_size=3, shuffle=False, collate_fn=collate_fn)

# define the lightning model
class ARCEncoder_Lightning(pl.LightningModule):
    def __init__(self, hidden_dim, num_layers, num_heads, max_examples):
        super(ARCEncoder_Lightning, self).__init__()
        self.model = ARCEncoder(hidden_dim, num_layers, num_heads, max_examples)
        self.head = nn.Linear(hidden_dim, 10)
        self.loss = nn.CrossEntropyLoss()

    def forward(self, xs, ys, ios, es, colors, sequence_lengths):
        return self.head(self.model(colors, xs, ys, es, ios, sequence_lengths))
    
    def random_masking_of_colors(self, batch):
        # randomly pick an input or an output from each problem and mask it
        xs, ys, ios, es, colors, sequence_lengths = batch
        batch_size = xs.size(0)
        masked_io = torch.randint(0, 2, (batch_size,))
        max_examples = torch.max(es, dim=1).values
        masked_example = (torch.randint(0, 1000, (batch_size,))% (max_examples+1))

        colors = colors.clone()
        masked_token = (es==masked_example.unsqueeze(-1)) & (ios==masked_io.unsqueeze(-1))
        colors[ masked_token ] = self.model.mask_index

        return colors, masked_token
    
    def training_step(self, batch, batch_idx):
        xs, ys, ios, es, original_colors, sequence_lengths = batch
        masked_colors, mask = self.random_masking_of_colors(batch)
        out = self(xs, ys, ios, es, masked_colors, sequence_lengths)

        prediction = out[mask]
        target = original_colors[mask]
        loss = self.loss(prediction, target)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        xs, ys, ios, es, original_colors, sequence_lengths = batch
        masked_colors, mask = self.random_masking_of_colors(batch)
        out = self(xs, ys, ios, es, masked_colors, sequence_lengths)

        prediction = out[mask]
        target = original_colors[mask]
        loss = self.loss(prediction, target)
        
        return loss
    
    def configure_optimizers(self):
        return optim.Adam(self.parameters(), lr=1e-4)

if __name__ == '__main__':
    model = ARCEncoder_Lightning(64, 4, 4, 12)
    trainer = pl.Trainer(max_epochs=10)
    trainer.fit(model, train_loader, validation_loader)