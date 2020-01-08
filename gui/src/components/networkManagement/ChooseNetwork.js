import React, { Component } from 'react';
import Dropdown from '../shared/dropdown'
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
          <button className="btn btn-primary float-left">Back</button>
        </Link>
        <Link to="/databaseContainer">
          <button className="btn btn-primary float-right">Next</button>
        </Link>
      </div>
    );
  }

}

export default ChooseNetwork; 