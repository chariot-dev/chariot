import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class NetworkManager extends Component {
  render() {
    return (
      <div class="container">
        <h1>Network Manager</h1>
          <text>Add, delete, or manage a network.</text>
          <br></br>
          <br></br>
          <br></br>
          <Link to="/addNetwork">
            <text>Add a Network</text>
          </Link>
          <br></br>
          <br></br>
          <Link to="/deleteNetwork">
            <text>Delete a Network</text>
          </Link>
          <br></br>
          <br></br>
          <Link to="/manageExistingNetworks">
            <text>Manage Existing Networks</text>
          </Link>

          <br></br>
          <br></br>

          <Link to="/welcome">
            <button class="btn btn-primary float-left">Back</button>
          </Link>   

      </div>
    );
  }


}
 
export default NetworkManager; 