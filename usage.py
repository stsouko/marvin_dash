import dash_marvinjs
import dash
from dash.dependencies import Input, Output
import dash_html_components as html

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_marvinjs.DashMarvinJS(
        id='input',
        marvin_url=app.get_asset_url('mjs/editor.html'),
        marvin_width=600
    ),
    html.Div(id='output')
])


@app.callback(Output('output', 'children'), [Input('input', 'structure')])
def display_output(value):
    return 'You have entered {}'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
