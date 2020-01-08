import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class NetworkManager extends Component {
  render() {
    return (
      <div className="container">
        <h1>Network Manager</h1>
          <p>Add, delete, or manage a network.</p>
          <br></br>
          
          <Link to="/addNetwork">Add a Network</Link>
          <br></br>
          <br></br>
          <Link to="/deleteNetwork">Delete a Network</Link>
          <br></br>
          <br></br>
          <Link to="/manageExistingNetworks">Manage Existing Networks</Link>

          <br></br>
          <br></br>

          <Link to="/welcome">
            <button className="btn btn-primary float-left">Back</button>
          </Link>   

      </div>
    );
  }


}
 
export default NetworkManager; 