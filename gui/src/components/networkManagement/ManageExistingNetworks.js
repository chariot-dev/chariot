import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class ManageExistingNetworks extends Component {
  render() {
    return (
      <div className="container">
        <h1>Manage Existing Networks</h1>
        <p>Select a network to modify its existing configuration settings.</p>
        <br></br>
        
        <Link to="/networkManager">
          <Button variant="primary" className="float-left">Back</Button>
        </Link>
      </div>
    );
  }


}

export default ManageExistingNetworks; 