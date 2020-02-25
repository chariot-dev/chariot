import React from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class ManageNetwork extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      networkName: this.props.location.networkProps["Network Name"], // this.props.location.networkProps obtained from jsx Link in ManageExistingNetworks
      deviceName: this.props.location.networkProps["Device Name"]
    }
  }


  render() {    
    return (
      <div className="container">
        <h1>{this.state.networkName}</h1>
        <p className="screenInfo">Choose between modifying the network- or device- specific configuration settings for {this.state.networkName}</p>

        <Link to={{pathname:"/manageExistingNetwork/" + this.state.networkName + "/networkConfiguration", networkProps:{'Network Name': this.state.networkName} }}>Edit Network Settings</Link>
        <br></br>
        <Link to={{pathname:"/manageExistingDevices/devices/" + this.state.networkName, networkProps:{'Network Name': this.state.networkName} }}>Edit Connected IoT Device Settings</Link>

        <br></br>

        <Link to="/manageExistingNetworks">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>
    );
  }
}

export default ManageNetwork;