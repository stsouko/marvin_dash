from chython import MRVRead, MRVWrite
from collections import namedtuple
from functools import wraps
from io import BytesIO, StringIO
from typing import Optional


Input = namedtuple('Input', ('structure', 'atoms', 'bonds'))


def prepare_input(idx: int = 0):
    """
    Decorate callback input. Converts MRV string into chython structures. None input propagated as is.

    :param idx: index of the MRV input.
    """
    def d(fn):
        @wraps(fn)
        def w(*args):
            if args[idx] is not None:
                args = list(args)

                if args[idx]['atoms']:
                    sa = tuple(int(x) for x in args[idx]['atoms'].split(','))
                else:
                    sa = ()
                if args[idx]['bonds']:
                    sb = tuple(tuple(int(x) for x in x.split('-')) for x in args[idx]['bonds'].split(','))
                else:
                    sb = ()

                with BytesIO(args[idx]['structure'].encode()) as f, MRVRead(f, ignore=True) as i:
                    try:
                        args[idx] = Input(next(i), sa, sb)
                    except StopIteration:
                        args[idx] = None
            return fn(*args)
        return w
    return d


def prepare_output(idx: Optional[int] = None):
    """
    Decorate callback output. Converts chython structures into MRV string. Use None for canvas cleaning.

    :param idx: index of the chython object in the output tuple for multiple outputs or None for single output.
    """
    def d(fn):
        @wraps(fn)
        def w(*args):
            out = fn(*args)
            s = out if idx is None else out[idx]
            if s is not None:
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
