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
      newDeviceNickname: this.props.params.newDeviceNickname,
      newDeviceDescription: this.props.params.newDeviceDescription,
      newDeviceType: this.props.params.newDeviceType,
      newDeviceName: "",
      newDeviceTime: "",
      newDevicePower: "",
      isSubmitted: false
    }

    this.handleChange = this.handleChange.bind(this);
    this.sendSpecificToForm = this.sendSpecificToForm.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
    
  }

  sendSpecificToForm(event) {
    this.props.onFormSubmit(this.state);
    event.preventDefault();
  }

  render() {
    return (
      <div>
        <br></br>
        <p className="screenInfo">Now please fill in the configuration fields for the {this.props.params.newDeviceType} device.</p> 

        
        <div className="form-group">
          <input className="form-control" id="newDeviceName" name="newDeviceName" placeholder="Name/IP Address" onChange={this.handleChange}/>
        </div>
        <div className="form-group">
          <input className="form-control" id="newDeviceTime" name="newDeviceTime" placeholder="Time" onChange={this.handleChange}/>
        </div>
        <div className="form-group">
          <input className="form-control" id="newDevicePower" name="newDevicePower" placeholder="Power" onChange={this.handleChange}/>
        </div>
        <br></br>




        <h1>FIELDS WILL BE DYNAMIC ACCORDING TO API CALL FOR THE DEVICE SELECTED</h1>
        <br></br>
        <br></br>


        
        <Button type="submit" variant="primary" className="float-right footer-button" onClick={this.sendSpecificToForm}>Next</Button>
      </div>
    );
  }
}

export default AddDeviceVars;