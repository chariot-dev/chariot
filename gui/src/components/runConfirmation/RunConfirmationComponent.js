import React, { Component } from 'react';
import { Link } from 'react-router-dom';

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
                <button className="btn btn-primary btn-lg float-left">Back</button>
            </Link>
            <button className="btn btn-primary btn-lg float-right">Begin Collection</button>
        </div>
    );
  }
  
}

export default RunConfirmationComponent;