import dash_marvinjs
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
from CGRtools.files import MRVRead, MRVWrite
from io import StringIO, BytesIO

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_marvinjs.DashMarvinJS(
        id='input',
        marvin_url=app.get_asset_url('mjs/editor.html'),  # URL of marvin distributive.
        # Note to correctly setup cross-domain headers on server!
        marvin_width='600px',
        marvin_height='600px'
    )
])


@app.callback(Output('input', 'upload'), [Input('input', 'download')])
def display_output(value):
    if value:  # data from `download` attr of widget
        with BytesIO(value.encode()) as f, MRVRead(f) as i:
            s = next(i)
            s.standardize()
            s.thiele()
        with StringIO() as f:
            with MRVWrite(f) as o:
                o.write(s)
            value = f.getvalue()
    return value  # send to `upload` attr of widget


if __name__ == '__main__':
    app.run_server(debug=True)
