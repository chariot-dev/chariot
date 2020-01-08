import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class ManageExistingNetworks extends Component {
  render() {
    return (
      <div className="container">
        <h1>Manage Existing Networks</h1>
        <p>Select a network to modify its existing configuration settings.</p>
        <br></br>
        
        <Link to="/networkManager">
          <button className="btn btn-primary float-left">Back</button>
        </Link>
      </div>
    );
  }


}

export default ManageExistingNetworks; 