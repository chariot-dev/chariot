import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class NetworkManager extends Component {
  render() {
    return (
      <div className="container">
        <h1>Network Manager</h1>
          <p className="screenInfo">Add, delete, or manage a network.</p>
          
          <div>
            <Link to="/addNetwork">Add a Network</Link>
            <br></br>
            <br></br>
            <Link to="/deleteNetwork">Delete a Network</Link>
            <br></br>
            <br></br>
            <Link to="/manageExistingNetworks">Manage Existing Networks</Link>
          </div>

          <Link to="/welcome">
            <Button variant="primary" className="float-left footer-button">Back</Button>
          </Link>
      </div>
    );
  }


}
 
export default NetworkManager; 