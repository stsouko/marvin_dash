from chython import MRVRead, MRVWrite, MoleculeContainer, ReactionContainer
from functools import wraps
from io import BytesIO, StringIO
from typing import Optional


def prepare_input(idx: int = 0):
    """
    Decorate callback input. Converts MRV string into chython structures.

    :param idx: index of the MRV input.
    """
    def d(fn):
        @wraps(fn)
        def w(*args):
            if args[idx] is not None:
                args = list(args)
                with BytesIO(args[idx].encode()) as f, MRVRead(f) as i:
                    try:
                        args[idx] = next(i)
                    except StopIteration:
                        args[idx] = None
            return fn(*args)
        return w
    return d


def prepare_output(idx: Optional[int] = None):
    """
    Decorate callback output. Converts chython structures into MRV string.

    :param idx: index of the chython object in the output tuple for multiple outputs or None for single output.
    """
    def d(fn):
        @wraps(fn)
        def w(*args):
            out = fn(*args)
            s = out if idx is None else out[idx]
            if isinstance(s, (MoleculeContainer, ReactionContainer)):
                with StringIO() as f:
                    with MRVWrite(f) as o:
                        o.write(s)
                    s = f.getvalue()
            if idx is None:
                return s
            out = list(out)
            out[idx] = s
            return tuple(out)
        return w
    return d


__all__ = ['prepare_input', 'prepare_output']
