from dash import Dash, html
from dash.dependencies import Input, Output
from dash_marvinjs import DashMarvinJS, prepare_input, prepare_output

app = Dash(__name__)

app.layout = html.Div([
    DashMarvinJS(
        id='input',
        marvin_url=app.get_asset_url('mjs/editor.html'),  # URL of marvin distributive.
        # Note to correctly setup cross-domain headers on server!
        marvin_width='600px',
        marvin_height='600px'
    )
])


@app.callback(Output('input', 'upload'), [Input('input', 'download')])
@prepare_input()
@prepare_output()
def display_output(value):
    if value:  # data from `download` attr of widget
        value.canonicalize()
    return value  # send to `upload` attr of widget


if __name__ == '__main__':
    app.run_server(debug=True)
