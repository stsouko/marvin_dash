# DashMarvinJS

DashMarvinJS is a Dash component library for ChemAxon MarvinJS integration.

Interaction of MJS with dash is done via the custom upload button on widget panel.

![](demo.png)

### Install from PyPI

    pip install dash_marvinjs

### Build from sources

1. Create a virtual env and activate.
    ```
    virtualenv venv
    . venv/bin/activate
    ```
2. Install python packages required to build components.
    ```
    pip install -r requirements.txt
    ```
3. Install npm packages
    ```
    npm install
    ```
4. Build your code:
    ```
    npm run build
    ```
5. Create a Python tarball
    ```
    python setup.py sdist
    ```
    This distribution tarball will get generated in the `dist/` folder
