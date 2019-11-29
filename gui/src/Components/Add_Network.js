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
            <input class="form-control" id="networkDescriptionInput"/>
          </div>
          <div>
            <Link to="/">
              <input type="submit" class="btn btn-primary float-right" value="Next"/>
            </Link>
          </div>
      </form>

    </div>
  );
}
  
export default Add_Network; 