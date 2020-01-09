import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class DeleteNetwork extends Component {
  render() {
    return (
      <div className="container">
        <h1>Delete an Existing Network</h1>
        <p>Select a network to delete.</p>
        <br></br>
        
        <Link to="/networkManager">
          <Button variant="primary" className="float-left">Back</Button>
        </Link>
      </div>
    );
  }

}

export default DeleteNetwork; 