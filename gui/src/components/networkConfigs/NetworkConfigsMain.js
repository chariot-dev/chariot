/*
  NetworkConfigsMain.js

  This component is the first screen the user will see when going to modify one of their 
  existing networks. The networks will be obtained via a GET request to the server.

*/

import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class NetworkConfigsMain extends Component {


  render() {
    return (
      <div className="container">
        <h1>Your Network Configurations</h1>
          <p className="screenInfo">Click on a network configuration to modify.</p>
          
          <Link to="/welcome">
            <Button variant="primary" className="float-left footer-button">Back</Button>
          </Link>
      </div>
    );
  }

}

export default NetworkConfigsMain; 