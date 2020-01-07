import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class ManageExistingNetworks extends Component {
  render() {
    return (
      <div className="container">
        <h1>Manage Existing Networks</h1>
        <text>Select a network to modify its existing configuration settings.</text>
        <br></br>
        <br></br>
        <Link to="/welcome">
          <button class="btn btn-primary float-left">Back</button>
        </Link>
      </div>
    );
  }


}

export default ManageExistingNetworks; 