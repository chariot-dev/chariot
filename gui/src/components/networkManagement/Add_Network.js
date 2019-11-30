import React from "react";
import { Link } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';

function Add_Network() {
  return (
    <div class="container">
      <h1>Add a New Network</h1>
        <text>Please fill in the fields below to create a network. Then, click "Next".</text>
        <br></br>
        <br></br>
        <form id="createNetworkForm">
          <div class="form-group">
            <label for="networkNameInput" class="font-weight-bold">Name:</label>
            <input class="form-control" id="networkNameInput"/>
          </div>
          <div class="form-group">
            <label for="networkDescriptionInput" class="font-weight-bold">Description:</label>
            <textarea class="form-control" id="networkDescriptionInput" rows="5"></textarea>
          </div>
          <Link to="/network_manager">
            <input type="button" class="btn btn-primary float-left" value="Back"/>
          </Link>         
          <Link to="/add_network_confirm">
            <input type="submit" class="btn btn-primary float-right" value="Next"/>
          </Link>
      </form>

    </div>
  );
}
  
export default Add_Network; 