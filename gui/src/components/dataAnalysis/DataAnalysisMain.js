import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class DataAnalysisMain extends Component {

  render() {
    return (
      <div className="container">
        <h1>Data Analysis</h1>
          <p className="screenInfo">Configure your data analysis options.</p>
          
          <Link to="/welcome">
            <Button variant="primary" className="float-left">Back</Button>
          </Link>        
      </div>
    );
  }

}

export default DataAnalysisMain; 