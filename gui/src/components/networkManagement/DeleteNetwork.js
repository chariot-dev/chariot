import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class DeleteNetwork extends Component {
  render() {
    return (
      <div className="container">
        <h1>Delete an Existing Network</h1>
          <text>Select a network to delete.</text>
        <br></br>
        <br></br>
        <Link to="/welcome">
          <button class="btn btn-primary float-left">Back</button>
        </Link>
      </div>
    );
  }

}

export default DeleteNetwork; 