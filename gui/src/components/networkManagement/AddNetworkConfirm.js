import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class AddNetworkConfirm extends Component {

  render() {
    return (
      <div class="container">
        <h1>Add a New Network</h1>
        <text>Please confirm that the information about the network is correct, then click "Create Network".</text>
        <br></br>
        <br></br>

        <text class="font-weight-bold">Name:</text>
        <br></br>
        <text class="font-weight-bold">Description:</text>
        <br></br>
        <br></br>
        <br></br>
        
        <Link to="/addNetwork">
          <button class="btn btn-primary float-left">Back</button>
        </Link>   
        <Link to="/networkManager">
          <button class="btn btn-primary float-right">Next</button>
        </Link>
      </div>
    );
  }

}
  
export default AddNetworkConfirm; 