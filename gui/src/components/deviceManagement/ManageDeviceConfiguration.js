import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';
import BaseURL from "../utility/BaseURL";

const getDeviceConfigurationBaseUrl = BaseURL + 'network/device';
const modifyDeviceConfigurationBaseUrl = BaseURL + 'network/device';
const deleteDeviceBaseUrl = BaseURL + 'network/device';
const getDeviceTypeConfiguration = BaseURL + 'network/device/config';
const uniqueDeviceId = "deviceId";

class ManageDeviceConfiguration extends Component {
  constructor(props) {
    super(props);
    this.state = {
      // These two state values are used to execute the GET call to get the device's original properties/configuration
      originalDeviceName : this.props.location.networkProps["Device Name"], // this.props.location.deviceProps obtained from prop passed through from Link in ManageExistingNetworks jsx element
      originalNetworkName : this.props.location.networkProps["Network Name"],
      originalDeviceProperties: {}, // Filled by componentDidMount()
      deviceConfiguration: {},
      newDeviceProperties: {},
      configurationFields: null,
      saveConfirmIsOpen: false,
      saveSuccessIsOpen: false,
      deleteConfirmIsOpen: false,
      deleteSuccessIsOpen: false
    }

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    var updatedDeviceProperties = this.state.newDeviceProperties; // Store from current state
    // with the inputType known, convert the value from text field to appropriate type
    var fieldType = event.target.type;
    var fieldVal = event.target.value;

    if (fieldType === "number") {
      fieldVal = parseInt(fieldVal)
    }
    else if (fieldType === "checkbox") {
      fieldVal = document.getElementById(event.target.id).checked;
    }
    updatedDeviceProperties[event.target.id] = fieldVal; // Update the json
    
    this.setState({ newDeviceProperties: updatedDeviceProperties }); // Update the state
  }


  // Gets run upon initial component render to load the default values of the text fields  
  componentDidMount() {
   fetch(getDeviceConfigurationBaseUrl + '?networkName=' + this.state.originalNetworkName + '&deviceId=' + this.state.originalDeviceName)
   .then(res => res.json())
   .then(
      // GET the values of the selected device
      (result) => {
        // this result gives
        var properties = result; // Response is a dictionary

        this.setState({originalDeviceProperties: properties});

        // Initialize all to-be-saved properties to be the original, in the event not all properties are modified so can still be saved
        this.setState({newDeviceProperties: properties});

        // Make another api call to get the device type's template configuration
        return fetch(getDeviceTypeConfiguration + '?deviceId=' + this.state.originalDeviceProperties["deviceType"])
      },
      // On error
      (error) => {
        console.log(error.message);
      }
    )
    .then(result => result.json())
    .then((result) => {
      var settings = result[this.state.originalDeviceProperties["deviceType"]]["settings"];

      var configurationFields = [];
      var deviceTypeIndex;

      this.setState({ deviceConfiguration : result });

      //combine originalDeviceProperties with result to have an object containing fields and their values
      for(var i = 0 ; i < settings.length; i++) {
        var currentAlias = settings[i].alias;

        if (currentAlias in this.state.originalDeviceProperties &&
            this.state.originalDeviceProperties[currentAlias] != null) {
          //combine the two
          settings[i].currentValue = this.state.originalDeviceProperties[currentAlias]
        }

        if (currentAlias === "deviceType") {
          //do not allow modification of deviceType
          deviceTypeIndex = i;
        }

        if (settings[i].settingsList) {
          for (var k = 0; k < settings[i].settingsList.length; k++) {
            var fieldJsonObj = {};
            var curFieldTitle = settings[i].settingsList[k].title;
            var curFieldAlias = settings[i].settingsList[k].alias;
            var curFieldDescription = settings[i].settingsList[k].description;
            var curFieldIsRequired = settings[i].settingsList[k].required;
            var curFieldType = settings[i].settingsList[k].inputType;

            fieldJsonObj["currentValue"] = "";
            fieldJsonObj["alias"] = curFieldAlias;
            fieldJsonObj['description'] = curFieldDescription;
            fieldJsonObj["required"] = curFieldIsRequired;
            fieldJsonObj["inputType"] = curFieldType;
            fieldJsonObj["title"] = curFieldTitle;
            if (curFieldTitle in this.state.originalDeviceProperties &&
                this.state.originalDeviceProperties[currentAlias] != null) {
              //combine the two
              settings[i].currentValue = this.state.originalDeviceProperties[currentAlias]
            }
            settings.push(fieldJsonObj);
          }
        }
      }

      //do not allow modification of deviceType
      settings.splice(deviceTypeIndex, 1);

      for(var j = 0 ; j < settings.length; j++) {
        var fieldAlias = settings[j].alias;
        var fieldIsRequired = settings[j].required;
        var valueType = settings[j].inputType;
        var fieldTitle = settings[j].title;

        configurationFields.push(
            <div className="form-group" key={settings[j].title + " Field" + j}>
              {fieldIsRequired ? <div className="requiredStar">*</div> : ""}
              {fieldTitle}: <input type={valueType} className={valueType === "checkbox" ? 'deviceCreationFormCheckbox' : 'form-control'}
                                      id={fieldAlias} name={fieldTitle} defaultValue={settings[j].currentValue} onChange={this.handleChange}/>
            </div>
        );
      }

      this.setState({ configurationFields: configurationFields });
    });
  }


  toggleDeletionConfirmationModal = () => {
    this.setState({ deleteConfirmIsOpen: !this.state.deleteConfirmIsOpen });
  }


  toggleModifyConfirmationModal = () => {
    this.setState({saveConfirmIsOpen: !this.state.saveConfirmIsOpen});
  }

  
  modifyDevice = () => {
    var data = {};

    if (this.state.originalDeviceName === this.state.newDeviceProperties[uniqueDeviceId]) {
      // if the device name is the same, can just use newDeviceProperties as data (remove fields with null)
      data = this.state.newDeviceProperties;
    }
    else {
      // if the device is not the same, then use the old name as "deviceId" and the new name as "newDeviceId"
      var originalName = this.state.originalDeviceName;
      var newName = this.state.newDeviceProperties[uniqueDeviceId];
      data = this.state.newDeviceProperties;

      delete this.state.newDeviceProperties[uniqueDeviceId];

      var tempNewDeviceProperties = this.state.newDeviceProperties;
      tempNewDeviceProperties["deviceId"] = originalName;
      tempNewDeviceProperties["newDeviceId"] = newName;

      this.setState ({ newDeviceProperties : tempNewDeviceProperties });
    }

    //add network name to payload to specify device on network
    data["networkName"] = this.state.originalNetworkName;
    //cannot have deviceType in modification api call
    delete data["deviceType"];

    //remove fields that are null
    for(var field in data) {
      if (data[field] === "" || data[field] === null) {
        delete data[field];
      }

    }
    
    // Put request options
    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };

    fetch(modifyDeviceConfigurationBaseUrl + "?networkName=" + this.state.originalNetworkName + "&deviceId=" + this.state.originalDeviceName, requestOptions)
    .then(
      () => {
        this.setState({
          saveConfirmIsOpen: false
        });
        this.setState({
          saveSuccessIsOpen: !this.state.successIsOpen
        });   
      },
      // If put was unsuccessful, update state and display error modal
      (error) => {
        console.log(error.message);
      }
    )
  }


  toggleDeletionSuccessModal = () => {
    // Delete request options
    const requestOptions = {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    };

    fetch(deleteDeviceBaseUrl + "?networkName=" + this.state.originalNetworkName + "&deviceId=" + this.state.originalDeviceName, requestOptions)
    .then(res => res.json())
    // On success
    .then(
      () => {
        this.setState({
          deleteConfirmIsOpen: false
        });
        this.setState({
          deleteSuccessIsOpen: !this.state.saveSuccessIsOpen
        });         
      },
      // On error
      (error) => {
        console.log(error.message);
      }
    )
  }
  
  
  hideSaveConfirmModal = () => {
    this.setState({saveConfirmIsOpen: false});
  }

  hideDeleteConfirmModal = () => {
    this.setState({deleteConfirmIsOpen: false});
  }


  render() {
    return [
      <div className="container" key="manageDeviceConfigurationScreen">
        <h1>{this.state.originalDeviceName} - Device Configuration</h1>
        <p className="screenInfo">Modifying configuration settings of {this.state.originalDeviceName} for {this.state.originalNetworkName}.</p>

        <form id="modifyDeviceForm">
          {this.state.configurationFields}
        </form>

        <Link to="/manageExistingNetworks">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>

        <Button variant="danger" className="footer-button button-mid-bottom" onClick={this.toggleDeletionConfirmationModal}>Delete Device</Button>

        <Button variant="success" className="float-right footer-button" onClick={this.toggleModifyConfirmationModal}>Save</Button>
      </div>,

      <Modal show={this.state.saveConfirmIsOpen} key="deviceSaveConfirmModal">
        <ConfirmationModalBody
          confirmationQuestion='Is the modified device configuration displayed below correct?'
          confirmationData = {this.state.newDeviceProperties}
          >
        </ConfirmationModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.hideSaveConfirmModal}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.modifyDevice}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.saveSuccessIsOpen} key="deviceSaveSuccessModal">
        <SuccessModalBody successMessage= {this.state.newDeviceProperties['deviceId'] + ' has successfully been modified.'}>
        </SuccessModalBody>
        <Modal.Footer>
          <Link to="/welcome">
            <Button variant="primary" className="float-right">Continue</Button>
          </Link>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.deleteConfirmIsOpen} key="deviceDeletionConfirmModal">
        <Modal.Body>
          To confirm the deletion of the device, {this.state.originalDeviceName}, click 'Yes'.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.hideDeleteConfirmModal}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleDeletionSuccessModal}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.deleteSuccessIsOpen} key="deviceDeletionSuccessModal">
        <SuccessModalBody successMessage= {this.state.originalDeviceName + " has been successfully removed from " + this.state.originalNetworkName}>
        </SuccessModalBody>
        <Modal.Footer>
          <Link to="/welcome">
            <Button variant="primary" className="float-right">Continue</Button>
          </Link>
        </Modal.Footer>
      </Modal>
    ]
  }
}

export default ManageDeviceConfiguration;