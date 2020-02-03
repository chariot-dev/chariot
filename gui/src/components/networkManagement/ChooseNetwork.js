/*


*/

import React, { Component } from 'react';
import Dropdown from '../shared/Dropdown';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

class ChooseNetwork extends Component {
  render() {
    return (
      <div className="container">
        <h1>Choose a Network</h1>
        <p className="screenInfo">Select a network to begin data collection process.</p>

        <Dropdown> </Dropdown>

        <Link to="/welcome">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
        <Link to="/databaseContainer">
          <Button variant="primary" className="float-right footer-button">Next</Button>
        </Link>
      </div>
    );
  }

}

export default ChooseNetwork; 