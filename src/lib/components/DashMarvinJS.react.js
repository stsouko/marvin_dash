import React, {Component} from 'react';
import PropTypes from 'prop-types';


export default class DashMarvinJS extends Component {
    componentDidUpdate(prevProps) {
        if (typeof this.marvin_sketcher !== 'undefined' && this.props.upload !== prevProps.upload) {
            this.marvin_sketcher.importAsMrv(this.props.upload);
        }
    }

    async send_download() {
        const mrv = await this.marvin_sketcher.exportStructure('mrv');
        if (mrv !== '<cml><MDocument></MDocument></cml>') {
            this.props.setProps({download: mrv});
        }
    }

    marvin_onready() {
        const sketcher = this.marvin_window.sketcherInstance;
        this.marvin_sketcher = sketcher;
        sketcher.addButton(this.props.marvin_button, this.send_download.bind(this));
    }

    marvin_onload(e) {
        const marvin = e.target.contentWindow.marvin;
        this.marvin_window = marvin;
        marvin.onReady(this.marvin_onready.bind(this));
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
    marvin_width: 900,
    marvin_height: 450,
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
    marvin_width: PropTypes.number,
    /**
     * Height of MarvinJS iframe.
     */
    marvin_height: PropTypes.number,

    /**
     * Button config of MarvinJS iframe.
     */
    marvin_button: PropTypes.shape({
        'name' : PropTypes.string,
        'image-url' : PropTypes.string,
        'toolbar' : PropTypes.string
    }),

    /**
     * Storage for structure from backend
     */
    upload: PropTypes.string,
    /**
     * Storage for structure to backend
     */
    download: PropTypes.string,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
