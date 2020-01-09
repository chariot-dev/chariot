import React, { Component } from 'react';
import Dropdown from '../shared/dropdown';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

class ChooseNetwork extends Component {
  render() {
    return (
      <div className="container">
        <h1>Choose a Network</h1>
        Select a network to begin data collection process.
        <br></br>
        <br></br>

        <Dropdown> </Dropdown>

        <br></br>
        <br></br>
        <Link to="/welcome">
          <Button variant="primary" className="float-left">Back</Button>
        </Link>
        <Link to="/databaseContainer">
          <Button variant="primary" className="float-right">Next</Button>
        </Link>
      </div>
    );
  }

}

export default ChooseNetwork; 