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

    this.state = {
      newDeviceNickname: props.params.newDeviceNickname,
      newDeviceDescription: props.params.newDeviceDescription,
      newDeviceType: props.params.newDeviceType,
      newDeviceTypeConfig: props.params.newDeviceTypeConfig, // Isn't being set for some reason. In cases below, references to props are used rather than state
      isSubmitted: false
    }

    this.handleChange = this.handleChange.bind(this);
    this.sendSpecificToForm = this.sendSpecificToForm.bind(this);
    this.componentDidUpdate = this.componentDidUpdate.bind(this);
  }

  componentDidUpdate() {
    if(this.state.newDeviceType !== this.props.params.newDeviceType ) {
      this.setState({ newDeviceType: this.props.params.newDeviceType });
    }
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  sendSpecificToForm(event) {
    this.props.onFormSubmit(this.state);
    event.preventDefault();
  }

  createDeviceFields() {
    console.log('in createDeviceFields');
    console.log(this.state);

    var deviceConfig = this.state.newDeviceTypeConfig[this.state.newDeviceType];
      
    var deviceSpecificForm = [];
    //var deviceDescription = deviceConfig["description"];
    var deviceSettings = deviceConfig["settings"];

    for (var i = 0; i < deviceSettings.length; i++) {
      var curFieldTitle = deviceSettings[i].title;
      var curFieldIsRequired = deviceSettings[i].required;

        if (curFieldIsRequired) {
          deviceSpecificForm.push(
            <div className="form-group" key={i}><input className="form-control" id={curFieldTitle} name={curFieldTitle} placeholder={curFieldTitle} onChange={this.handleChange}/></div>
          );
        }
        else {
          deviceSpecificForm.push(
            <div className="form-group" key={i}><input className="form-control" id={curFieldTitle} name={curFieldTitle} placeholder={curFieldTitle} onChange={this.handleChange}/></div>
          );
        }
    }

    console.log('leaving createDeviceFields');
    return (deviceSpecificForm);
    
  }


  render() {
    return (
      <div>
        <br></br>
        <p className="screenInfo">Now please fill in the configuration fields for the {this.state.newDeviceType} device.</p> 

        {this.createDeviceFields()}

        <Button type="submit" variant="primary" className="float-right footer-button" onClick={this.sendSpecificToForm}>Next</Button>
      </div>
    );
  }
}

export default AddDeviceVars;