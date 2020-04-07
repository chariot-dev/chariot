import React, {Component} from 'react';

class DataCollectionEpisodeStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chosenNetwork: this.props.location.networkProps['Network Name'],
      networkDevices: this.props.location.networkProps['Devices'],
    }
  }


  render() {
    console.log(this.state);

    return [
      <div className="container">
        <h1>Data Collection Episode</h1>
        <p>Data collection episode for {this.state.chosenNetwork}.</p>
        <div id="deviceCollectionStatuses">
        
        </div>

      </div>
    ]
  }
}

export default DataCollectionEpisodeStatus;