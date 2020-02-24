import React from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class ManageNetwork extends React.Component {
  constructor(props) {
    super(props);
    this.state = {}
  }


  render() {
    return (
      <div className="container">
        <h1>{this.props.location.deviceProps["Device Name"]}</h1>
        <p className="screenInfo">Modifying configuration settings of {this.props.location.deviceProps["Device Name"]} for {this.props.location.deviceProps["Network Name"]}.</p>


        <Link to="/manageExistingNetworks">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>
    );
  }
}

export default ManageNetwork;