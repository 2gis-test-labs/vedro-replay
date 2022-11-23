import os
from vedro import params


def replay(requests_file: str):
    assert os.path.exists(requests_file)

    def wrapped(fn):
        with open(requests_file) as f:
            for request in f.read().splitlines():
                params(request)(fn)
        return fn

    return wrapped
