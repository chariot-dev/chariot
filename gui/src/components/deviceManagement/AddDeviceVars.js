/*
  AddDeviceVars.js

  This component is shown inside the AddDeviceHome component containing the dynamically generated
  configuration fields of a device depending on the user's choice of device.

*/

import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';

class AddDeviceVars extends Component {
  constructor (props) {
    super(props);
    
    // Initializing newDeviceTypeConfigVals (the json to hold the config values of the device-specific parameters)
    var deviceConfig = props.params.newDeviceTypeGeneralVals.newDeviceTypeConfig[props.params.newDeviceTypeGeneralVals['Device Type']];
    var deviceSettings = deviceConfig["settings"];
    var initializedNewDeviceTypeConfigVals = {};
    for (var i = 0; i < deviceSettings.length; i++) {
      var curFieldTitle = deviceSettings[i].title; 
      initializedNewDeviceTypeConfigVals[curFieldTitle] = '';
    }

    // Setting the initial state
    this.state = {
      newDeviceTypeGeneralVals: {
        'Device Nickname': props.params.newDeviceTypeGeneralVals['Device Nickname'],
        'Device Description': props.params.newDeviceTypeGeneralVals['Device Description'],
        'Device Type': props.params.newDeviceTypeGeneralVals['Device Type'],
        newDeviceTypeConfig: props.params.newDeviceTypeGeneralVals.newDeviceTypeConfig
      },
      newDeviceTypeConfigVals: initializedNewDeviceTypeConfigVals,
      isSubmitted: false
    }

    this.handleChange = this.handleChange.bind(this);
    this.sendSpecificToForm = this.sendSpecificToForm.bind(this);
  }

  handleChange(event) {
    // Remove spaces from variable name and replace with %20 to create state attribute variable
    var updatedNewDeviceTypeConfigVals = this.state.newDeviceTypeConfigVals; // Store from current state
    updatedNewDeviceTypeConfigVals[event.target.name] = event.target.value; // Update the json
    this.setState({ newDeviceTypeConfigVals: updatedNewDeviceTypeConfigVals }); // Update the state
  }

  sendSpecificToForm(event) {
    this.props.onFormSubmit(this.state);
    event.preventDefault();
  }

  createDeviceFields = () => {
    var deviceConfig = this.state.newDeviceTypeGeneralVals.newDeviceTypeConfig[this.state.newDeviceTypeGeneralVals['Device Type']];
    var deviceSpecificForm = [];
    var deviceSettings = deviceConfig["settings"];

    console.log(deviceSettings);

    for (var i = 0; i < deviceSettings.length; i++) {
      var curFieldTitle = deviceSettings[i].title;
      var curFieldIsRequired = deviceSettings[i].required;
      console.log(curFieldIsRequired + '   ' + curFieldTitle);

      deviceSpecificForm.push(
        <div className="form-group" key={i}><input required={curFieldIsRequired} className="form-control" id={curFieldTitle} name={curFieldTitle} placeholder={curFieldTitle} onChange={this.handleChange}/></div>
      );
    }

    return (deviceSpecificForm);
  }


  render() {
    return (
      <div>
        <br></br>
        <p className="screenInfo">Now please fill in the configuration fields for the {this.state.newDeviceTypeGeneralVals['Device Type']} device.</p> 

        {this.createDeviceFields()}

        <Button type="submit" variant="primary" className="float-right footer-button" onClick={this.sendSpecificToForm}>Next</Button>
      </div>
    );
  }
}

export default AddDeviceVars;