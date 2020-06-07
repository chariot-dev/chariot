import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import socketIOClient from "socket.io-client";

import NetworkDeviceCellScreenTemplate from '../shared/NetworkDeviceCellScreenTemplate';
import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';

const getAllDbConfigsBaseUrl = 'http://localhost:5000/chariot/api/v1.0/database/all';
const databaseTestUrl = "http://localhost:5000/chariot/api/v1.0/database/test";

class ChooseDatabaseConfig extends Component {
  constructor(props) {
    super(props);

    this.state = {
      chosenNetwork: this.props.location.networkProps["Network Name"],
      chosenNetworkDevices: this.props.location.networkProps["Devices"],
      existingConfigs: [],
      testSuccessIsOpen: false,
      testErrorIsOpen: false,
      testErrorMessage: ""
    }

    this.hideTestSuccessModal = this.hideTestSuccessModal.bind(this);
    this.hideTestErrorModal = this.hideTestErrorModal.bind(this);
  }

  componentDidMount() {
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
          updatedDbJsonArray['chosenNetworkDevices'] = this.state.chosenNetworkDevices;

          this.setState({ existingConfigs: updatedDbJsonArray });
        },
        // On error
        (error) => {
          console.log(error.message);
        }
      )
  }

  hideTestSuccessModal(event) {
    this.setState({ testSuccessIsOpen: false });
    event.preventDefault();
  }

  hideTestErrorModal(event) {
    this.setState({ testErrorIsOpen: false });
    event.preventDefault();
  }

  // Callback from child, NetworkDeviceCellScreen
  testDatabaseConnection = (curDatabaseId, curDatabaseName, curDatabaseType, curDatabaseHost, curDatabaseUsername, curDatabasePassword) => {
    var data = {
      "dbId": curDatabaseId,
      "host": curDatabaseHost,
      "databaseName": curDatabaseName,
      "type": curDatabaseType,
    }

    if (curDatabaseUsername) {
      data["username"] = curDatabaseUsername;
    }
    if (curDatabasePassword) {
      data["password"] = curDatabasePassword;
    }

    // Post request options
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };

    // fetch request to test database connection
    fetch(databaseTestUrl, requestOptions)
      .then(
        (res) => {
          if (res.status === 400) { // If 400 error was returned from the api call
            return res.json(); // Return the response to the next then()
          }
          else { // If a 400 wasn't returned, then the api call was successful
            this.setState({ testSuccessIsOpen: true }); // Set to true so test connection success modal appears
            return; // Since going to then(), return null since no need to parse response
          }
        })
      .then(
        (resJson) => {
          if (resJson) { // If the response exists (coming from 400 error)
            this.setState({ testErrorMessage: resJson.message }, () => { // Set the error message
              this.setState({ testErrorIsOpen: true }); // Then set test error modal to true
            });
          }
        })
  }

  render() {
    return [
      <div className="container">
        <h1>Choose a Database</h1>
        <p className="screenInfo">
          Select a database to begin data collection process. If you haven't created a database configuration yet, please create one.
        </p>

        {this.state.existingConfigs.length > 0 ?
          <NetworkDeviceCellScreenTemplate dataJson={this.state.existingConfigs} withLinks={false} type="chooseDatabase" testDatabaseConnection={this.testDatabaseConnection}></NetworkDeviceCellScreenTemplate> : <p>No existing database configurations were found.</p>}

        <Link to={{ pathname: "/chooseNetwork" }}>
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>

        <Link to={{ pathname: "/databaseConnection", networkProps: { "Network Name": this.state.chosenNetwork, "Devices": this.state.chosenNetworkDevices } }}>
          <Button variant="success" className="float-right footer-button">Create</Button>
        </Link>
      </div>,

      <Modal show={this.state.testSuccessIsOpen} key="testDatabaseConfigSuccessModal">
        <SuccessModalBody successMessage="Chariot connected to the database succesfully!">
        </SuccessModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-right" onClick={this.hideTestSuccessModal}>OK</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.testErrorIsOpen} key="testDatabaseConfigErrorModal">
        <ErrorModalBody errorMessage={this.state.testErrorMessage}>
        </ErrorModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-right" onClick={this.hideTestErrorModal}>OK</Button>
        </Modal.Footer>
      </Modal>

    ]
  }

}

export default ChooseDatabaseConfig;