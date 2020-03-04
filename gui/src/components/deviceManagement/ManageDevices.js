import React from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class ManageDevices extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      networkName: this.props.location.networkProps["Network Name"], // this.props.location.networkProps obtained from jsx Link in ManageExistingNetworks
    }
  }


  render() {    
    return (
      <div className="container">
        <h1>{this.state.networkName}'s Devices</h1>
        <p className="screenInfo">Choose a device from {this.state.networkName} to manage.</p>



        <Link to="/manageExistingNetworks">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>
    );
  }
}

export default ManageDevices;