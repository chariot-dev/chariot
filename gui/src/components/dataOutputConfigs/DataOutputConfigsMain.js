import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class DataOutputConfigsMain extends Component {

  render() {
    return (
      <div className="container">
        <h1>Your Data Output Configs</h1>
          <p></p>
          <br></br>
          <Link to="/welcome">
            <Button variant="primary" className="float-left">Back</Button>
          </Link>
      </div>
    );
  }

}

export default DataOutputConfigsMain; 