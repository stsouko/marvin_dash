from chython import MoleculeContainer, ReactionContainer, smiles
from dash import Dash, html
from dash.dependencies import Input, Output
from dash_marvinjs import DashMarvinJS, prepare_input, prepare_output
from typing import Tuple, Optional, Union


app = Dash(__name__)

app.layout = html.Div([
    DashMarvinJS(
        id='mjs',
        marvin_url=app.get_asset_url('mjs/editor.html'),  # URL of marvin distributive.
        # Note to correctly setup cross-domain headers on server!
        marvin_license={'url': app.get_asset_url('license.cxl'), 'is_dynamic': False},
        marvin_width='600px',
        marvin_height='600px'
    )
])


@app.callback(Output('mjs', 'output'), [Input('mjs', 'input')])
@prepare_input()
@prepare_output()
def display_output(inp: Optional[Tuple[Union[MoleculeContainer, ReactionContainer],
                                       Tuple[int, ...],
                                       Tuple[Tuple[int, int], ...]]]) -> Union[MoleculeContainer,
                                                                               ReactionContainer, None]:
    if inp:
        s = inp.structure
        s.canonicalize()

        print([s.atom(x) for x in inp.atoms])
        print([s.bond(x, y) for x, y in inp.bonds])
        if 'Se' in s:  # erase fragrant molecule!
            return MoleculeContainer()
        return s
    else:
        s = smiles('CC(I)C')
        s.clean2d()
        return s


if __name__ == '__main__':
    app.run_server(debug=True)
