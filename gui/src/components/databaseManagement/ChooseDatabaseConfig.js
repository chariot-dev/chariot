import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

import NetworkDeviceCellScreenTemplate from '../shared/NetworkDeviceCellScreenTemplate';

const getAllDbConfigsBaseUrl = 'http://localhost:5000/chariot/api/v1.0/database/all';

class ChooseDatabaseConfig extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingConfigs: []
    }
  }

  componentDidMount () {
    fetch(getAllDbConfigsBaseUrl)
    .then(res => res.json())
    .then(
      // On success
      (result) => {
        var responseJsonArray = result; // Response is a dictionary

        var updatedDbJsonArray = this.state.existingConfigs;

        for (var i = 0; i < responseJsonArray.length; i++) {
          updatedDbJsonArray.push(responseJsonArray[i]);
        }

        this.setState({ existingConfigs: updatedDbJsonArray });
      },
      // On error
      (error) => {
        console.log(error.message);


       /*
         Have an error modal for being unable to get device types. Once button on the modal is clicked, Chariot goes back to welcome screen
       */
      }
    )
  }

  render() {
    return (
      <div className="container">
        <h1>Choose a Database</h1>
        <p className="screenInfo">
          Select a database to begin data collection process.
        </p>

        {this.state.existingConfigs ? <NetworkDeviceCellScreenTemplate dataJson={this.state.existingConfigs} withLinks={false} type="choose"></NetworkDeviceCellScreenTemplate> : null}

        <Link to="/welcome">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>
    );
  }

}

export default ChooseDatabaseConfig;