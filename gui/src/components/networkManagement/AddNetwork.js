import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class AddNetwork extends Component {
  render() {
    return (
      <div className="container">
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
            <Link to="/networkManager">
              <button class="btn btn-primary float-left">Back</button>
            </Link>         
            <Link to="/addNetworkConfirm">
              <button class="btn btn-primary float-right">Next</button>
            </Link>
        </form>
      </div>
    );
  }

}

export default AddNetwork; 