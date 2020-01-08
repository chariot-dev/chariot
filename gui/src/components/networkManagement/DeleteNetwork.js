import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class DeleteNetwork extends Component {
  render() {
    return (
      <div className="container">
        <h1>Delete an Existing Network</h1>
        <p>Select a network to delete.</p>
        <br></br>
        
        <Link to="/networkManager">
          <button className="btn btn-primary float-left">Back</button>
        </Link>
      </div>
    );
  }

}

export default DeleteNetwork; 