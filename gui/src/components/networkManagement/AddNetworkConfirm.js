import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class AddNetworkConfirm extends Component {

  render() {
    return (
      <div className="container">
        <h1>Add a New Network</h1>
        <p>Please confirm that the information about the network is correct, then click "Create Network".</p>
        <br></br>

        <b>Name:</b>
        <br></br>
        <b>Description:</b>
        <br></br>
        <br></br>
        <br></br>
        
        <Link to="/addNetwork">
          <button className="btn btn-primary float-left">Back</button>
        </Link>   
        <Link to="/networkManager">
          <button className="btn btn-primary float-right">Create Network</button>
        </Link>
      </div>
    );
  }

}
  
export default AddNetworkConfirm; 