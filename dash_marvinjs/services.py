from chython import MRVWrite, smiles, SDFRead, RDFRead, SMILESRead
from io import StringIO
from itertools import chain
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
        for r in (SMILESRead, RDFRead, SDFRead):
            for s in r(StringIO(data)):
                s.clean2d()
                with StringIO() as f:
                    with MRVWrite(f) as o:
                        o.write(s, skip_mapping=skip_mapping)
                    return {'structure': f.getvalue()}
        return {'structure': None}


__all__ = ['importer']
