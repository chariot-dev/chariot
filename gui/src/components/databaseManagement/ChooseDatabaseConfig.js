import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

import NetworkDeviceCellScreenTemplate from '../shared/NetworkDeviceCellScreenTemplate';

import BaseURL from "../utility/BaseURL";

const getAllDbConfigsBaseUrl = BaseURL + 'database/all';

class ChooseDatabaseConfig extends Component {
  constructor(props) {
    super(props);

    this.state = {
      chosenNetwork: this.props.location.networkProps["Network Name"],
      existingConfigs: []
    }
  }

  componentDidMount () {
    fetch(getAllDbConfigsBaseUrl)
    .then(res => res.json())
    .then(
      // On success
      (result) => {
        var responseJson = result; // Response is a dictionary

        var updatedDbJsonArray = this.state.existingConfigs;

        // Create a json for the database config
        for (var key of Object.keys(responseJson)) {
          updatedDbJsonArray.push(responseJson[key]);
        }

        // Add the chosen network to the database config
        updatedDbJsonArray['chosenNetwork'] = this.state.chosenNetwork;

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

        {this.state.existingConfigs ?
          <NetworkDeviceCellScreenTemplate dataJson={this.state.existingConfigs} chosenNetwork={this.state.chosenNetwork} withLinks={false} type="chooseDatabase"></NetworkDeviceCellScreenTemplate> : null}

        <Link to={{pathname: "/chooseNetwork"}}>
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>

        <Link to={{ pathname: "/databaseConnection", "Network Name": this.state.chosenNetwork }}>
          <Button variant="success" className="float-right footer-button">Create</Button>
        </Link>
      </div>
    );
  }

}

export default ChooseDatabaseConfig;
