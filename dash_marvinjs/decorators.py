from chython import MRVRead, MRVWrite, ReactionContainer, MoleculeContainer
from dataclasses import dataclass
from functools import wraps
from io import BytesIO, StringIO
from typing import Optional, Union, List, Tuple


@dataclass
class Input:
    structure: Union[MoleculeContainer, ReactionContainer, None]
    atoms: Union[List[int], List[Tuple[int, int]], None] = None
    bonds: Union[List[Tuple[int, int]], List[Tuple[int, int, int]], None] = None


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
                            mp = dict(enumerate(((y, x) for y, x in enumerate(s.molecules()) for x in x), 1))
                            sb = [(*mp[x], mp[y][1]) for x, y in sb]
                        else:  # molecule
                            mp = dict(enumerate(s, 1))
                            sb = [(mp[x], mp[y]) for x, y in sb]
                        args[idx] = Input(s, [mp[x] for x in sa], sb)
            return fn(*args)
        return w

    if callable(idx):  # decorated function
        f, idx = idx, 0
        return d(f)
    return d


def prepare_output(idx: Optional[int] = None, skip_mapping: bool = True):
    """
    Decorate callback output. Converts chython structures into MRV string. Use None for canvas cleaning.

    :param idx: index of the chython object in the output tuple for multiple outputs or None for single output.
    :param skip_mapping: remove atom numbers.
    """
    def d(fn):
        @wraps(fn)
        def w(*args):
            out = fn(*args)
            s = out if idx is None else out[idx]
            if s is not None:
                if isinstance(s, (MoleculeContainer, ReactionContainer)):
                    s = Input(s)
                elif isinstance(s, Input):
                    if s.structure is None:
                        s = {'structure': None}
                        if idx is None:
                            return s
                        out = list(out)
                        out[idx] = s
                        return tuple(out)
                    elif isinstance(s.structure, MoleculeContainer):
                        mp = {x: n for n, x in enumerate(s.structure, 1)}
                        if (bonds := s.bonds) is not None:
                            bonds = ','.join(f'{mp[x]}-{mp[y]}' for x, y in bonds)
                    elif isinstance(s.structure, ReactionContainer):
                        mp = {nx: m for m, nx in
                              enumerate(((n, x) for n, x in enumerate(s.structure.molecules()) for x in x), 1)}
                        if (bonds := s.bonds) is not None:
                            bonds = ','.join(f'{mp[(n, x)]}-{mp[(n, y)]}' for n, x, y in bonds)
                    else:
                        raise TypeError('MoleculeContainer, ReactionContainer or None expected')

                    if (atoms := s.atoms) is not None:
                        atoms = ','.join(str(mp[x]) for x in atoms)
                    s = Input(s.structure, atoms, bonds)
                else:
                    raise TypeError('dash_marvinjs.Input or MoleculeContainer or ReactionContainer expected')
                with StringIO() as f:
                    with MRVWrite(f, mapping=not skip_mapping) as o:
                        o.write(s.structure)
                    s = {'structure': f.getvalue(), 'atoms': s.atoms, 'bonds': s.bonds}
            if idx is None:
                return s
            out = list(out)
            out[idx] = s
            return tuple(out)
        return w

    if callable(idx):  # decorated function
        f, idx = idx, None
        return d(f)
    return d


__all__ = ['prepare_input', 'prepare_output', 'Input']
