import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class NetworkConfigsMain extends Component {


  render() {
    return (
      <div className="container">
        <h1>Your Network Configs</h1>
          <p className="screenInfo">Click on a network config to modify.</p>
          
          <Link to="/welcome">
            <Button variant="primary" className="float-left">Back</Button>
          </Link>
      </div>
    );
  }

}

export default NetworkConfigsMain; 