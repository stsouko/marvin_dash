from chython import MRVWrite, smiles, mdl_mol, mdl_rxn
from io import StringIO
from flask import request


def importer(app, route='/importer', skip_mapping=True):
    """
    SMILES, SDF, RDF importer

    :param app: dash app
    :param route: url for binding
    :param skip_mapping: skip import of atom to atom mapping
    """
    @app.server.route(route, methods=['POST'])
    def callback():
        data = request.json['structure']
        for r in (smiles, mdl_mol, mdl_rxn):
            try:
                s = r(data)
            except ValueError:
                continue

            s.clean2d()
            with StringIO() as f:
                with MRVWrite(f, mapping=not skip_mapping) as o:
                    o.write(s)
                return {'structure': f.getvalue()}
        return {'structure': None}


__all__ = ['importer']
