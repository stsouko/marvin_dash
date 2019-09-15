import React, {Component} from 'react';
import PropTypes from 'prop-types';


export default class DashMarvinJS extends Component {
    render() {
        const {id, marvin_url, marvin_width, marvin_height, setProps} = this.props;

        function marvin_events() {
            const sketcher = this.marvin.sketcherInstance;
            const button = {
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
            };
            sketcher.addButton(button, async () => {
                const mrv = await sketcher.exportStructure('mrv');
                if (mrv !== '<cml><MDocument></MDocument></cml>') {
                    setProps({structure: mrv});
                }
            });
        }
        function marvin_ready(e) {
            const marvin = e.target.contentWindow.marvin;
            marvin.onReady(marvin_events.bind({marvin: marvin}));
        }

        return (
            <div id={id}>
                <iframe id='marvinjs_sketch'
                        src={marvin_url}
                        width={marvin_width}
                        height={marvin_height}
                        data-toolbars='reaction'
                        onLoad={marvin_ready}
                />
            </div>
        );
    }
}

DashMarvinJS.defaultProps = {
    marvin_width: 900,
    marvin_height: 450,
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
     * Size of MarvinJS iframe.
     */
    marvin_width: PropTypes.number,
    marvin_height: PropTypes.number,

    /**
     * The value displayed in the input.
     */
    structure: PropTypes.string,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
