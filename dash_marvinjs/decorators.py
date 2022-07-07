from chython import MRVRead, MRVWrite, ReactionContainer
from collections import namedtuple
from functools import wraps
from io import BytesIO, StringIO
from typing import Optional


Input = namedtuple('Input', ('structure', 'atoms', 'bonds'))


def prepare_input(idx: int = 0):
    """
    Decorate callback input. Converts MRV string into chython structures and process selected atoms and bonds.
    None input propagated as is.

    Output format:

    (MoleculeContainer, [selected atoms numbers], [(bonds atoms numbers, pairs)])
     or
    (ReactionContainer, [(molecule index, selected atom number)], [(molecule index, bonds atoms numbers, pairs)])

    :param idx: index of the MJS input in Dash callback.
    """
    def d(fn):
        @wraps(fn)
        def w(*args):
            if (ai := args[idx]) is not None:
                sa = [int(x) for x in ai['atoms'].split(',')] if ai['atoms'] else []
                sb = [[int(x) for x in x.split('-')] for x in ai['bonds'].split(',')] if ai['bonds'] else []

                args = list(args)
                with BytesIO(ai['structure'].encode()) as f, MRVRead(f, ignore=True) as i:
                    try:
                        s = next(i)
                    except StopIteration:
                        args[idx] = None
                    else:
                        if isinstance(s, ReactionContainer):
                            mp = dict(enumerate(((y, x) for y, x in enumerate(s.molecules()) for x in x), start=1))
                            sb = [(*mp[x], mp[y][1]) for x, y in sb]
                        else:  # molecule
                            mp = dict(enumerate(s, start=1))
                            sb = [(mp[x], mp[y]) for x, y in sb]
                        args[idx] = Input(s, [mp[x] for x in sa], sb)
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
