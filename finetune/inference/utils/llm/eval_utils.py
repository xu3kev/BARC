#!/usr/bin/env python
# coding=utf-8

# ====== check test io ======

import contextlib, io, signal
@contextlib.contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")

    signal.setitimer(signal.ITIMER_REAL, seconds)
    signal.signal(signal.SIGALRM, signal_handler)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


@contextlib.contextmanager
def swallow_io():
    stream = WriteOnlyStringIO()
    with contextlib.redirect_stdout(stream):
        with contextlib.redirect_stderr(stream):
            with redirect_stdin(stream):
                yield stream

class TimeoutException(Exception):
    pass


class WriteOnlyStringIO(io.StringIO):
    """StringIO that throws an exception when it's read from"""

    def read(self, *args, **kwargs):
        raise OSError

    def readline(self, *args, **kwargs):
        raise OSError

    def readlines(self, *args, **kwargs):
        raise OSError

    def readable(self, *args, **kwargs):
        """Returns True if the IO object can be read."""
        return False


class redirect_stdin(contextlib._RedirectStream):  # type: ignore
    _stream = "stdin"

def eval_code(line, timeout=3., return_exec_globals=False, exec_globals=None):
    try:
        exec_globals = {} if exec_globals is None else exec_globals
        with swallow_io() as s:
            with time_limit(timeout):
                exec(line, exec_globals)
        if return_exec_globals:
            return exec_globals
        else:
            return 'passed'
    except TimeoutException:
        return 'timed out'
    except BaseException as e:
        return f"failed: {e}\nPrinted outputs: {s.getvalue()}"
