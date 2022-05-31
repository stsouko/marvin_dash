import React, {Component} from 'react';
import PropTypes from 'prop-types';


export default class DashMarvinJS extends Component {
    componentDidUpdate(prevProps) {
        if (typeof this.marvin_sketcher !== 'undefined' &&
            this.props.output !== null &&
            this.props.output !== prevProps.output) {
            this.marvin_sketcher.importAsMrv(this.props.output);
        }
    }

    async send_download() {
        const mrv = await this.marvin_sketcher.exportStructure('mrv');
        const {atoms, bonds} = this.marvin_sketcher.getSelection();
        this.props.setProps({input: {structure: mrv, atoms: atoms, bonds: bonds}});
    }

    marvin_onready() {
        const {url, is_dynamic} = this.props.marvin_license;
        this.marvin_window.Sketch.license(url, is_dynamic);
        this.marvin_sketcher = this.marvin_window.sketcherInstance;
        this.marvin_sketcher.addButton(this.props.marvin_button, this.send_download.bind(this));
    }

    marvin_onload(e) {
        this.marvin_window = e.target.contentWindow.marvin;
        this.marvin_window.onReady(this.marvin_onready.bind(this));
    }

    render() {
        const {id, marvin_url, marvin_width, marvin_height} = this.props;

        return (
            <div id={id}>
                <iframe id='marvinjs_sketch'
                        src={marvin_url}
                        width={marvin_width}
                        height={marvin_height}
                        data-toolbars='reaction'
                        onLoad={this.marvin_onload.bind(this)}
                />
            </div>
        );
    }
}

DashMarvinJS.defaultProps = {
    marvin_width: '900',
    marvin_height: '450',
    marvin_button: {
        'name' : 'Upload',
        'image-url' : 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAMAAAD04JH5AAAArlBMVEUAAAAAAAA' +
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' +
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' +
                      'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABeyFOlAAAAAXRSTlMAQObYZgAAAAFiS0' +
                      'dEAIgFHUgAAAAJcEhZcwAACcUAAAnFAYeExPQAAAAHdElNRQfjCQwVADLJ+C5eAAABUklEQVR42u3ZQWrDMBC' +
                      'F4TlMIFun2JD//hdLodBFLamWrMlL2jc7WWbmi2LkEY44FRsQulj4ClV9vkNdXyMArQC0AtAKQCsArQC0AtAK' +
                      'QCsArQC0AtAKQCsArQC0AtAKQCsArWBfojpIESz7AvVRhqCQvjGcD9gK2Vvj6YJS7uaFXECtLX8WoH4uSHwIC' +
                      'olpX1vTj2HFX5u3Eezzlpc7cTP+ua61/zth/V/zcGqAAQZkAY63ea25bbRZ7Ok06zMfzSzXevlLV69bnViGW2' +
                      'bmAH5Ncxvv/I8AtuFTwyTAgTT3KUfvEwDeFrDOeQjHASEGHN2IkgBrx1Z8GpDxMjLAAAMMMMAAAwwwwAADDDD' +
                      'AAAMMMODvAaLzO3EmIDSAGLt7IqDvO3EKoCcMMMAAAwwwwAADDDDAgPcCZIcBBrwmIP4RoLJTXNWAUNePuInr' +
                      'f8b92eUfelqXBAH/Tb4AAAAASUVORK5CYII=',
        'toolbar' : 'N'
    },
    marvin_license: {
        'url': '/license.cxl',
        'is_dynamic': false
    }
};

DashMarvinJS.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * A URL of MarvinJS iframe.
     */
    marvin_url: PropTypes.string.isRequired,

    /**
     * Width of MarvinJS iframe.
     */
    marvin_width: PropTypes.string,
    /**
     * Height of MarvinJS iframe.
     */
    marvin_height: PropTypes.string,

    /**
     * Button config of MarvinJS iframe.
     */
    marvin_button: PropTypes.shape({
        'name' : PropTypes.string,
        'image-url' : PropTypes.string,
        'toolbar' : PropTypes.string
    }),

    /**
     * License location
     */
    marvin_license: PropTypes.shape({
        'url': PropTypes.string,
        'is_dynamic': PropTypes.bool
    }),

    /**
     * Structure from backend for rendering.
     */
    output: PropTypes.string,

    /**
     * Structure and selected atoms/bonds.
     */
    input: PropTypes.shape({
        'structure': PropTypes.string,
        'atoms': PropTypes.string,
        'bonds': PropTypes.string
    }),

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
