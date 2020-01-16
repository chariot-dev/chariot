import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class RunConfirmationComponent extends Component {

  render() {
    return (
        <div className="container">
            <div>
                <h1> Data Collection Configuration Confirmation </h1>
                <p> You have selected the following configuration for the data collection episode: </p>
            </div>
            <div className="text-center">
                <p> Network Name: </p>
            </div>
            <div className="text-center">
                <p> Database Details </p>
            </div>
            <Link to="/databaseContainer">
                <Button variant="primary" className="float-left footer-button">Back</Button>
            </Link>
            <Button variant="primary" className="float-right footer-button">Begin Collection</Button>
        </div>
    );
  }
  
}

export default RunConfirmationComponent;