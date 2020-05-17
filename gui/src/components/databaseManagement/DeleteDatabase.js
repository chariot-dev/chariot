/*
  The component that handles the functinality for deleting a network. The body of the screen (network/device info)
  is generated through NetworkDeviceCellScreenTemplate as the child component, and uses a callback to update this 
  component's state. deleteNetwork={this.deleteConfirmation.bind(this)} is passed as a callback to 
  NetworkDeviceCellScreenTemplate. When the 'Delete Network' is pressed in the child (NetworkDeviceCellScreenTemplate), 
  it calls this.props.deleteNetwork.bind(this, curNetworkName), which in turn, calls deleteConfirmation(selectedNetwork) 
  in the parent (this component).
*/

import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import NetworkDeviceCellScreenTemplate from '../shared/NetworkDeviceCellScreenTemplate';

import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';

const dbConfigsBaseUrl = 'http://localhost:5000/chariot/api/v1.0/database';

class DeleteDatabase extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingDatabaseConfigurations: [],
      selectedDatabaseConfigurationToDelete: null,
      confirmIsOpen: false,
      successIsOpen: false,
      errorIsOpen: false,
      errorMessage: ""
    }

    this.hideErrorModal = this.hideErrorModal.bind(this);
    this.hideConfirmationModal = this.hideConfirmationModal.bind(this);
  } 

  // Get all db configs before rendering component
  componentDidMount () {
    fetch(dbConfigsBaseUrl + "/all")
    .then(res => res.json())
    .then(
      // On success
      (receivedDBConfigs) => {
        console.log(receivedDBConfigs);
        var dbConfigJson = receivedDBConfigs; // Response is a JSON OBJECT for this one, not JSON ARRAY like the others
        var updatedDatabaseConfigurationsJsonArray = this.state.existingDatabaseConfigurations;

        for (var key in dbConfigJson) {
          updatedDatabaseConfigurationsJsonArray.push(dbConfigJson[key]);
        }

        this.setState({ existingDatabaseConfigurations: updatedDatabaseConfigurationsJsonArray });

      },
      // On error
      (error) => {
        console.log(error.message);
      }
    )
  }


  hideErrorModal(event) {
    this.setState({ errorIsOpen: !this.state.errorIsOpen });    
    event.preventDefault();
  }

  hideConfirmationModal(event) {
    this.setState({ confirmIsOpen: !this.state.confirmIsOpen }); 
  }


  deleteConfirmation(selectedDatabaseConfigurationToDelete) {
    this.setState({confirmIsOpen: true});
    this.setState({selectedDatabaseConfigurationToDelete: selectedDatabaseConfigurationToDelete});
  }


  deleteDatabaseConfiguration = () => {
    console.log("Delete the db");

    // Delete request options
    const requestOptions = {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    };

    fetch(dbConfigsBaseUrl + "?dbId=" + this.state.selectedDatabaseConfigurationToDelete, requestOptions)
    .then(
      (res) => {
        if (res.status === 400) { // If not 200, something went wrong, so go to the next then()
          return res.json();
        }
        else { // If a 400 wasn't returned, then the api call was successful
          this.setState({ confirmIsOpen: false });
          this.setState({ successIsOpen: !this.state.successIsOpen });
          return; // Since going to then(), return null since no need to parse response
        }
      })
      // On error
      .then(
        (resJson) => {
          if (resJson) { // If the response exists (coming from 400 error)
            this.setState({ confirmIsOpen: false });
            this.setState({ errorMessage: resJson.message }, () => { // Set the error message
              this.setState({ errorIsOpen: true }); // Then set test error modal to true
            }); 
          }
        }
      )
  }


  render() {
    console.log(this.state);
    return [
      <div className="container" key="deleteDatabaseConfigurationScreen">
        <h1>Delete an Existing Database Configuration</h1>
        <p className="screenInfo">
          Select a database configuration to delete.
        </p>
        
        {this.state.existingDatabaseConfigurations ? <NetworkDeviceCellScreenTemplate dataJson={this.state.existingDatabaseConfigurations} withLinks={false} type="deleteDatabase" deleteDatabaseConfiguration={this.deleteConfirmation.bind(this)}></NetworkDeviceCellScreenTemplate> : null}

        <Link to="/databaseManager">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>,
      <Modal show={this.state.confirmIsOpen} onHide={this.hideConfirmationModal} key="datababseDeletionConfirmModal">
        <Modal.Body>
          To confirm the deletion of the database configuration for {this.state.selectedDatabaseConfigurationToDelete}, click 'Yes'.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.hideConfirmationModal}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.deleteDatabaseConfiguration}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.successIsOpen} key="databaseConfigurationDeletionSuccessModal">

      <SuccessModalBody successMessage="The database configuration has been deleted!">
      </SuccessModalBody>

      <Modal.Footer>
        <Link to="/databaseManager">
          <Button variant="primary" className="float-right">Continue</Button>
        </Link>
      </Modal.Footer>
    </Modal>,

    <Modal show={this.state.errorIsOpen} key="databaseConfigurationDeletionErrorModal">

      <ErrorModalBody errorMessage={this.state.errorMessage}>
      </ErrorModalBody>

      <Modal.Footer>
        <Button variant="primary" className="float-left" onClick={this.hideErrorModal}>OK</Button>
      </Modal.Footer>
    </Modal>

    ]
  }

}

export default DeleteDatabase; 