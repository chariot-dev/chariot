/*
  AddDeviceVars.js

  This component is shown inside the AddDeviceHome component containing the dynamically generated
  configuration fields of a device depending on the user's choice of device.

*/

import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
/*
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

  }



  render() {
    console.log(this.state.newDeviceNickname);
    console.log(this.state.newDeviceDescription);
    console.log(this.state.newDeviceType);
    console.log(this.state.newDeviceTypeConfig);
    console.log(this.props.params.newDeviceTypeConfig);

    return (
      <div>
        
      </div>
    );
  }
}
*/



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
  }

  componentDidUpdate() {
    if(this.state.newDeviceTypeConfig !== this.props.params.newDeviceTypeConfig ) {
      this.setState({ newDeviceTypeConfig: this.props.params.newDeviceTypeConfig });
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
    console.log("============");
    /*
    console.log(this.state.newDeviceNickname);
    console.log(this.state.newDeviceDescription);
    console.log(this.state.newDeviceType);
    */
    console.log(this.state);
    console.log(this.state.newDeviceType);
    console.log(this.state.newDeviceTypeConfig);
    console.log(this.props.params.newDeviceTypeConfig);
    console.log(Object.keys(this.state.newDeviceTypeConfig).length);

    var deviceType = this.state.newDeviceType;
    var deviceConfig;
    if  (this.state.newDeviceType == "ImpinjSpeedwayR420") 
      deviceConfig = this.state.newDeviceTypeConfig["Impinj Speedway R420"]; // HARDCODED UNTIL EITHER SPACES ARE REMOVED FROM BACKEND, OR SPACES ARE ADDED TO FRONT END
    else if  (this.state.newDeviceType == "ImpinjxArray") 
      deviceConfig = this.state.newDeviceTypeConfig["Impinj xArray"]; // HARDCODED UNTIL EITHER SPACES ARE REMOVED FROM BACKEND, OR SPACES ARE ADDED TO FRONT END

      
    if (deviceConfig) { // Doing this for now because issue of API call semmingly firing twice. Also, body executes while newDeviceTypeConfig is null. Concurrency/Async
      var deviceSpecificForm = [];
      var deviceDescription = deviceConfig["description"];
      var deviceSettings = deviceConfig["settings"];
      console.log(deviceSettings);


      for (var i = 0; i < deviceSettings.length; i++) {
        var curFieldTitle = deviceSettings[i].title;
        var curFieldIsRequired = deviceSettings[i].required;

          if (curFieldIsRequired) {
            deviceSpecificForm.push(
              <div className="form-group"><input key={i} className="form-control" id={curFieldTitle} name={curFieldTitle} placeholder={curFieldTitle} onChange={this.handleChange}/></div>);
          }
          else {
            deviceSpecificForm.push(
              <div className="form-group"><input key={i} className="form-control" id={curFieldTitle} name={curFieldTitle} placeholder={curFieldTitle} onChange={this.handleChange}/></div>);
          }
      }

      console.log(deviceSpecificForm);

      return (deviceSpecificForm);
    }


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