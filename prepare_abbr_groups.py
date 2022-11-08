from chython import SDFRead
from chython.utils import to_rdkit_molecule
from rdkit.Chem import SDWriter, CreateMolSubstanceGroup
from sys import argv

if len(argv) != 4:
    print('prepare_abbr_groups.py input.sdf out.sdf metadata_title_entry')

name = argv[3]

with SDFRead(argv[1]) as f, SDWriter(argv[2]) as o:
    for m in f:
        r = to_rdkit_molecule(m, keep_mapping=False)
        r.SetProp('_Name', m.meta[name])
        s = CreateMolSubstanceGroup(r, 'SUP')
        for n in range(len(m)):
            s.AddAtomWithIdx(n)
        s.SetProp('LABEL', m.meta[name])
        s.SetProp('ESTATE', 'E')
        o.write(r)
