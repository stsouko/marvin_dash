from chython import MoleculeContainer, ReactionContainer, smiles
from dash import Dash, html
from dash.dependencies import Input, Output
from dash_marvinjs import DashMarvinJS, prepare_input, prepare_output, Input as MJSInput, importer
from typing import Optional, Union


app = Dash(__name__)

app.layout = html.Div([
    DashMarvinJS(
        id='mjs',
        marvin_url=app.get_asset_url('mjs/editor.html'),  # URL of marvin distributive.
        # Note to correctly setup cross-domain headers on server!
        marvin_license={'url': app.get_asset_url('license.cxl'), 'is_dynamic': False},
        marvin_width='600px',
        marvin_height='600px',
        marvin_services={'molconvertws': '/importer'}  # default
    )
])

importer(app, '/importer', True)  # setup importer route and mapping display


@app.callback(Output('mjs', 'output'), [Input('mjs', 'input')])
@prepare_input  # or prepare_input(idx=0)
@prepare_output  # or prepare_output(idx=None, skip_mapping=True)
def callback(inp: Optional[MJSInput]) -> Union[MJSInput, MoleculeContainer, ReactionContainer, None]:
    if inp:
        if not isinstance((s := inp.structure), MoleculeContainer):
            # clean canvas example
            return MJSInput(None)

        s.canonicalize()
        if len(inp.atoms) == 2 and len(inp.bonds) == 1:
            if s.atom(inp.atoms[0]).atomic_symbol == 'C' and s.atom(inp.atoms[1]).atomic_symbol == 'C':
                if s.bond(*inp.bonds[0]).order == 2:
                    return inp  # return structure and selection
        return s  # return structure without selection
    else:  # page loaded. render default structure
        s = smiles('C=C(I)C')
        s.clean2d()
        return s


if __name__ == '__main__':
    app.run_server(debug=True)
