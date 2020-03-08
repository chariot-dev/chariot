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

    console.log(deviceSettings.length);

    for (var i = 0; i < deviceSettings.length; i++) {
      var fieldJsonObj = {};
      var curFieldTitle;
      var curFieldAlias;
      var curFieldDescription;
      var curFieldIsRequired;

      if (deviceSettings[i].settingsList) {
        for (var k = 0; k < deviceSettings[i].settingsList.length; k++) {
          curFieldTitle = deviceSettings[i].settingsList[k].title;
          curFieldAlias = deviceSettings[i].settingsList[k].alias;
          curFieldDescription = deviceSettings[i].settingsList[k].description;
          curFieldIsRequired = deviceSettings[i].settingsList[k].required;
          var curFieldType = deviceSettings[i].settingsList[k].inputType;

          fieldJsonObj["value"] = "";
          fieldJsonObj["alias"] = curFieldAlias;
          fieldJsonObj['description'] = curFieldDescription;
          fieldJsonObj["required"] = curFieldIsRequired;
          fieldJsonObj["inputType"] = curFieldType;

          initializedNewDeviceTypeConfigVals[curFieldTitle] = (fieldJsonObj);

          console.log(curFieldTitle);
        }
      }
      else {
        curFieldTitle = deviceSettings[i].title;
        curFieldAlias = deviceSettings[i].alias;

        // for now, hide deviceType field since it was chosen by the dropdown
        if (curFieldAlias !== "deviceType") {
          curFieldDescription = deviceSettings[i].description;
          curFieldIsRequired = deviceSettings[i].required;

          fieldJsonObj["value"] = "";
          fieldJsonObj["alias"] = curFieldAlias;
          fieldJsonObj['description'] = curFieldDescription;
          fieldJsonObj["required"] = curFieldIsRequired;

          // speedwayR420 needs this check
          if ("inputType" in deviceSettings[i]) {
            fieldJsonObj["inputType"] = deviceSettings[i].inputType
          }

          initializedNewDeviceTypeConfigVals[curFieldTitle] = (fieldJsonObj);

          console.log(curFieldTitle);
        }
      }

      console.log(initializedNewDeviceTypeConfigVals);
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

    console.log(initializedNewDeviceTypeConfigVals);

    this.handleChange = this.handleChange.bind(this);
    this.sendSpecificToForm = this.sendSpecificToForm.bind(this);
  }


  handleChange(event) {
    // Remove spaces from variable name and replace with %20 to create state attribute variable
    var updatedNewDeviceTypeConfigVals = this.state.newDeviceTypeConfigVals; // Store from current state
    updatedNewDeviceTypeConfigVals[event.target.name].value = event.target.value; // Update the json
    this.setState({ newDeviceTypeConfigVals: updatedNewDeviceTypeConfigVals }); // Update the state
  }


  // Couldn't call onFormSubmit() explicitly on click. Needed event.preventDefault()
  sendSpecificToForm(event) {
    this.props.onFormSubmit(this.state);
    event.preventDefault();
  }


  createDeviceFields = () => {
    //var deviceConfig = this.state.newDeviceTypeGeneralVals.newDeviceTypeConfig[this.state.newDeviceTypeGeneralVals['Device Type']];
    var deviceSpecificForm = [];
    var deviceSettings = this.state.newDeviceTypeConfigVals;

    console.log(deviceSettings);

    for (var key in deviceSettings) {
      var curFieldAlias = deviceSettings[key].alias;
      var curFieldIsRequired = deviceSettings[key].required;
      var valueType = deviceSettings[key].inputType;

      if (valueType == "checkbox") {
        deviceSpecificForm.push(
          <div className="form-group" key={curFieldAlias}>
            <input type={valueType}  required={curFieldIsRequired} className="deviceCreationFormCheckbox" id={curFieldAlias} name={key} placeholder={key} onChange={this.handleChange}/>
            <label> {key}</label>
          </div>
        );
      }
      else {
        deviceSpecificForm.push(
          <div className="form-group" key={curFieldAlias}>
            <label>{key}:</label>
            <input type={valueType}  required={curFieldIsRequired} className="form-control" id={curFieldAlias} name={key} placeholder={key} onChange={this.handleChange}/>
          </div>
        );
      }

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