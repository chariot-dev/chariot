import React, { Component } from "react";
import { Link } from "react-router-dom";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";

import ErrorModalBody from "../shared/ErrorModalBody";

const dataCollectionBaseURL = "http://localhost:5000/chariot/api/v1.0/data";

class RunConfirmationComponent extends Component {
  constructor(props) {
    super(props);

    this.state = {
      "Network Name": this.props.location.networkProps["Network Name"],
      Devices: this.props.location.networkProps["Devices"],
      "Database ID": this.props.location.networkProps["Database ID"],
      "Database Name": this.props.location.networkProps["Database Name"],
      "Database Type": this.props.location.networkProps["Database Type"],
      configurationSettings: {}, // Contains configId and runTime
      errorIsOpen: false,
      errorMessage: "",
    };

    this.handleChange = this.handleChange.bind(this);
    this.hideErrorModal = this.hideErrorModal.bind(this);
  }

  hideErrorModal(event) {
    this.setState({ errorIsOpen: false });
    event.preventDefault();
  }

  startDataCollection = () => {
    var data = {
      dbId: this.state["Database ID"],
      networkName: this.state["Network Name"],
      configId: this.state.configurationSettings["configId"],
      runTime: parseInt(this.state.configurationSettings["runTime"]),
    };

    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    };

    // Execute the post request to 'postCreateNetworkBaseUrl' with 'requestOptions' using fetch
    fetch(dataCollectionBaseURL, requestOptions)
      .then((res) => res.json())
      .then(
        // If post was successful, then the dataCollector has been created, proceed to visualizer
        (result) => {
          if (result.success === true) {
            // Success
            return; // Since going to then(), return null since no need to parse message
          } else if (result.message) {
            // If got a message, then failed
            return result;
          }
        }
      )
      .then((res) => {
        if (res) {
          // Set up state to display error modal upon rerender
          this.setState({ errorMessage: res.message }, () => {
            // Set the error message
            this.setState({ errorIsOpen: true }); // Then set test error modal to true
          });
        }
        else {
          // Success, so make API to start data collection then send to visualizer
          fetch(
            dataCollectionBaseURL +
            "/start?configId=" +
            this.state.configurationSettings["configId"]
          )
            .then((res) => res.json())
            .then(
              // On success
              (result) => {
                this.props.history.push({
                  pathname: "/dataCollectionEpisodeStatus",
                  runProps: {
                    "Network Name": this.state["Network Name"],
                    Devices: this.state["Devices"],
                    configId: this.state.configurationSettings["configId"],
                  },
                });
              },
              // On error
              (error) => {
                this.setState({ errorMessage: error.message }, () => {
                  // Set the error message
                  this.setState({ errorIsOpen: true }); // Then set test error modal to true
                });
              }
            );
        }
      });
  };

  // Update state when text field is updated
  handleChange(event) {
    var updatedConfigurationSettings = this.state.configurationSettings; // Store from current state
    updatedConfigurationSettings[event.target.id] = event.target.value; // Update the json

    this.setState({ configurationSettings: updatedConfigurationSettings }); // Update the state
  }

  render() {
    return [
      <div className="container">
        <div>
          <h1> Data Collection Configuration Confirmation </h1>
          <p>
            {" "}
            You have selected the following configuration for the data
            collection episode:{" "}
          </p>
        </div>
        <div>
          <p>
            {" "}
            <b>Network Name:</b> {this.state["Network Name"]}
          </p>
        </div>
        <div>
          <p>
            {" "}
            <b>Database ID:</b> {this.state["Database ID"]}{" "}
          </p>
        </div>
        <div>
          <p>
            {" "}
            <b>Database Name:</b> {this.state["Database Name"]}{" "}
          </p>
        </div>
        <div>
          <p>
            {" "}
            <b>Database Type:</b> {this.state["Database Type"]}{" "}
          </p>
        </div>

        <form>
          <div className="form-group">
            Run Time:{" "}
            <input
              type="number"
              className="form-control"
              id="runTime"
              onChange={this.handleChange}
            />
          </div>
          <div className="form-group">
            Configuration Name:{" "}
            <input
              className="form-control"
              id="configId"
              onChange={this.handleChange}
            />
          </div>

          <Link to="/chooseNetwork">
            <Button variant="primary" className="float-left footer-button">
              Back
            </Button>
          </Link>
          <Button
            variant="primary"
            className="float-right footer-button"
            onClick={this.startDataCollection}
          >
            Begin Collection
          </Button>
        </form>
      </div>,

      <Modal show={this.state.errorIsOpen} key="runError">
        <ErrorModalBody errorMessage={this.state.errorMessage}></ErrorModalBody>

        <Modal.Footer>
          <Button
            variant="primary"
            className="float-right"
            onClick={this.hideErrorModal}
          >
            OK
          </Button>
        </Modal.Footer>
      </Modal>,
    ];
  }
}

export default RunConfirmationComponent;
