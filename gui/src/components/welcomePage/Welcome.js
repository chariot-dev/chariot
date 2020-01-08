import React, { Component } from 'react';
import { Link } from 'react-router-dom';

import './Welcome.css';

class Welcome extends Component {

  render() {
    return (
      <div className="container" id="welcomeContent">
        <br></br>
        <div>
          <img alt="Account Avatar" className="accountAvi" src="data:image/png;base64,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"></img>
        </div>
        <div className="accountInfo">
          <b>Name: </b> John Doe <br></br>
          <div>
            <Link to="/networkConfigsMain" id="networkConfigsMainLink">View Network Configs</Link>
            <br></br>
            <Link to="/deviceConfigsMain" id="deviceConfigsMainLink">View IoT Device Configs</Link>
            <br></br>
            <Link to="/dataOutputConfigsMain" id="dataOutputConfigsMainLink">View Data Output Configs</Link>
          </div>
          <br></br>
          <div>
            <Link to="/">
              <button className="btn btn-primary">Log Out</button>
            </Link>
          </div>
        </div>
        <br></br>
        <br></br>

        <div>
          <Link to="/networkManager">Network Manager</Link>
          <br></br>
          View, create, delete, modify, or manage your existing networks.
        </div>

        <br></br>

        <div>
          <Link to="/dataAnalysisMain">Perform Data Analysis</Link>
          <br></br>
          Select a storage unit and perform data analysis.
        </div>

        <br></br>
        <br></br>

        <Link to="/chooseNetwork">
          <button type="button" className="btn btn-primary container">Configure Data Collection</button>
        </Link>

      </div>
    );
  }

}

export default Welcome; 
