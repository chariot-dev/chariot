import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';

const databaseConfigurationBaseUrl = 'http://localhost:5000/chariot/api/v1.0/database';

class ManageDatabaseConfiguration extends Component {
  constructor(props) {
    super(props);
    this.state = {
      originalDatabaseId: this.props.location.databaseProps["Database Id"],
      originalDatabaseProperties: {}, // Filled by componentDidMount
      newDatabaseProperties: {},
      userDefinedFields: [], // Take note of user defined database fields so that's all the user has to worry about
      newUserDefinedProperties: {}, // Used for display in the confirmation modal
      databaseTypeConfigTemplate: {},
      confirmIsOpen: false,
      successIsOpen: false
    }

    this.handleChange = this.handleChange.bind(this);
    this.hideConfirmationModal = this.hideConfirmationModal.bind(this);
    this.toggleConfirmationModal = this.toggleConfirmationModal.bind(this);
    this.forceSuccessModalInteraction = this.forceSuccessModalInteraction.bind(this);
  }


  // Gets run upon initial component render to load the default values of the text fields  
  componentDidMount() {
    fetch(databaseConfigurationBaseUrl + "?dbId=" + this.state.originalDatabaseId)
      .then(res => res.json())
      .then(
        // GET the original properties of the selected database configuration
        (result) => {
          var originalDatabasePropertiesJson = result;

          this.setState({ originalDatabaseProperties: { ...originalDatabasePropertiesJson } });

          // Initialize all to-be-saved properties to be the original, in the event not all properties are modified so can still be saved
          this.setState({ newDatabaseProperties: { ...originalDatabasePropertiesJson } });

          return fetch(databaseConfigurationBaseUrl + "/config?dbId=" + this.state.originalDatabaseProperties['type'])
        },
        // On error
        (error) => {
          console.log(error.message);
        }
      )
      .then(result => result.json())
      .then(
        (templateConfigJson) => {
          this.setState({ databaseTypeConfigTemplate: templateConfigJson });
          var userFields = [];

          for (var i = 0; i < templateConfigJson[this.state.originalDatabaseProperties["type"]]["settings"].length; i++) {
            var curSetting = templateConfigJson[this.state.originalDatabaseProperties["type"]]["settings"];
            var curFieldAlias = curSetting[i].alias;
            userFields.push(curFieldAlias);
          }

          this.setState({ userDefinedFields: userFields });
        }
      )
  }

  createTextFields = () => {
    var databaseModificationForm = []; // Will contain the html form for modifying the database's settings
    var userFields = [];

    for (var i = 0; i < this.state.databaseTypeConfigTemplate[this.state.originalDatabaseProperties["type"]]["settings"].length; i++) {
      var curSetting = this.state.databaseTypeConfigTemplate[this.state.originalDatabaseProperties["type"]]["settings"];
      var curFieldAlias = curSetting[i].alias;
      var curFieldType = curSetting[i].inputType;
      var curFieldTitle = curSetting[i].title;
      var curFieldIsRequired = curSetting[i].required;
      var isDisabled = false;
      if (curFieldAlias === "type") {
        isDisabled = true;
      }

      userFields.push(curFieldAlias);

      databaseModificationForm.push(
        <div className="form-group" key={curFieldAlias}>
          {curFieldIsRequired ? <div className="requiredStar">*</div> : ""}
          {curFieldTitle}
          <input type={curFieldType} required={curFieldIsRequired} disabled={isDisabled} className='form-control' id={curFieldAlias} name={curFieldTitle} defaultValue={this.state.originalDatabaseProperties[curFieldAlias]} onChange={this.handleChange} />
        </div>
      );
    }

    return databaseModificationForm;
  }

  hideConfirmationModal(event) {
    this.setState({ confirmIsOpen: !this.state.confirmIsOpen });
  }

  forceSuccessModalInteraction(event) {
    return; // Do nothing because need user to click "continue"
  }

  handleChange(event) {
    var updatedDatabaseProperties = this.state.newDatabaseProperties; // Store from current state
    var fieldVal = event.target.value;

    updatedDatabaseProperties[event.target.id] = fieldVal; // Update the json

    this.setState({ newDatabaseProperties: updatedDatabaseProperties });

    if (this.state.newDatabaseProperties['dbId'] !== this.state.originalDatabaseId) {
      var temp = this.state.newDatabaseProperties;
      temp['newDbId'] = this.state.newDatabaseProperties['dbId'];
      temp['dbId'] = this.state.originalDatabaseId;
      this.setState({ newDatabaseProperties: temp });
    }
  }


  toggleConfirmationModal(event) {
    this.setState({ confirmIsOpen: !this.state.confirmIsOpen });
    event.preventDefault();
  }


  updateDatabaseConfiguration = () => {
    var data = this.state.newDatabaseProperties;

    // According to api, don't include these fields if not necessary
    if (!this.state.originalDatabaseProperties['password'] && !data['password']) {
      delete data['password'];
    }
    if (!this.state.originalDatabaseProperties['username'] && !data['username']) {
      delete data['username'];
    }
    delete data['port'];
    delete data['tableName'];
    delete data['timeoutMS'];
    delete data['type'];

    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };

    fetch(databaseConfigurationBaseUrl, requestOptions)
      .then(
        () => {
          this.setState({ confirmIsOpen: false });
          this.setState({ successIsOpen: !this.state.successIsOpen });
        },
        // If put was unsuccessful, update state and display error modal
        (error) => {

        }
      )
  }

  render() {
    return [
      <div className="container" key="newDeviceScreen">
        <h1>{this.state.originalDatabaseId} - Database Configuration</h1>
        <p className="screenInfo">Modifying the database configuration settings of {this.state.originalDatabaseId}.</p>

        <form onSubmit={this.toggleConfirmationModal}>
          {this.state.databaseTypeConfigTemplate[this.state.originalDatabaseProperties["type"]] ? this.createTextFields() : null}

          <Link to="/manageExistingDatabaseConfigurations">
            <Button variant="primary" className="float-left footer-button">Back</Button>
          </Link>

          <Button variant="primary" className="float-right footer-button" type="submit">Save</Button>
        </form>

      </div>,

      <Modal show={this.state.confirmIsOpen} onHide={this.hideConfirmationModal} key="modifyDatabaseConfigurationConfirmationModal">
        <ConfirmationModalBody
          confirmationQuestion='Are updated database configuration settings displayed below correct?'
          confirmationData={this.state.newDatabaseProperties}
        >
        </ConfirmationModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.toggleConfirmationModal}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.updateDatabaseConfiguration}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.successIsOpen} onHide={this.forceSuccessModalInteraction} key="modifyDatabaseConfigurationSettingsSuccessModal">
        <SuccessModalBody successMessage='The database configuration was succesfully modified! Click "Continue" to go back to the "Database Manager" screen.'>
        </SuccessModalBody>

        <Modal.Footer>
          <Link to="/databaseManager">
            <Button variant="primary" className="float-left">Continue</Button>
          </Link>
        </Modal.Footer>
      </Modal>

    ]
  }

}


export default ManageDatabaseConfiguration; 