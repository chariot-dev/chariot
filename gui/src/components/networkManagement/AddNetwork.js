import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class AddNetwork extends Component {
  render() {
    return (
      <div className="container">
        <h1>Add a New Network</h1>
          <p>Please fill in the fields below to create a network. Then, click "Next".</p>
          <br></br>
          
          <form id="createNetworkForm">
            <div className="form-group">
              <input className="form-control" id="networkNameInput" placeholder="Name"/>
            </div>
            <div className="form-group">
              <textarea className="form-control" id="networkDescriptionInput" rows="5" placeholder="Description"></textarea>
            </div>
            <Link to="/networkManager">
              <button className="btn btn-primary float-left">Back</button>
            </Link>         
            <Link to="/addNetworkConfirm">
              <button className="btn btn-primary float-right">Next</button>
            </Link>
        </form>
      </div>
    );
  }

}

export default AddNetwork; 