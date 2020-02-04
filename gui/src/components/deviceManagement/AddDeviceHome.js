/*
  AddDeviceHome.js

  This component is the first screen the user will see when creating a device.
  This component handles the GUI for creating a device, as well as the modals 
  that appear as the process is completed. In order to get the specific
  device fields, AddDeviceVars is a child component.

  Currently, only a single device can be created before the user is sent back
  to the Welcome screen.
*/

import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import AddDeviceVars from './AddDeviceVars';


class AddDeviceHome extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newDeviceNickname: "", // Nickname attribute for device
      newDeviceDescription: "", // Description for device
      newDeviceType: "", // Type of device
      showDeviceSpecificSettings: false, // Whether or not the type of device has been chosen by the user already
      isSubmitted: false, // Whether or not the device information is ready to be sent to the server
      confirmIsOpen: false, // Is the confirm modal open?
      successIsOpen: false, // Is the success modal open?
      deviceSpecificState: {}, // User-defined device attributes
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleDeviceTypeChange = this.handleDeviceTypeChange.bind(this);
  }

  // ============ DEVICE-SPECIFIC FIELDS ARE CURRENTLY HARD-CODED ================
  handleNewDeviceCreation = (submittedDeviceSpecificState) => {
    this.setState ({ deviceSpecificState: submittedDeviceSpecificState })

    console.log(this.state.newDeviceNickname);
    console.log(this.state.newDeviceDescription);
    console.log(this.state.newDeviceType);
    console.log(submittedDeviceSpecificState.newDeviceName);
    console.log(submittedDeviceSpecificState.newDeviceTime);
    console.log(submittedDeviceSpecificState.newDevicePower);
    console.log(this.state.deviceSpecificState); // Values are delayed in console. Will show up on second "Next" click

    this.setState({
      isSubmitted: !this.state.isSubmitted,
      confirmIsOpen: !this.state.confirmIsOpen
    }); 
  }
 
  /*
    Updates prop values (device-related) as they are entered by the user.
  */  
  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  /*
    As the device type the user selects changes, update that in the state.
  */
  handleDeviceTypeChange(event) {
    // Update chosen device type
    this.setState({[event.target.name]: event.target.value});

    // Boolean to show the device type's-specific settings to true
    this.setState({
      showDeviceSpecificSettings: true
    });
  }

  /*
    Function that launches the success modal after the user confirms the device
    information that they entered is correct. Also makes the POST request to the
    server to create the new device.
  */
  toggleSuccessModal = () => {
    this.setState({
      confirmIsOpen: false
    });
    this.setState({
      successIsOpen: !this.state.successIsOpen
    });



  }

  /* 
    Called when the user either submits the registration form by clicking "Next"
    in the AddDeviceVars component or "No" on the confirmation modal. Will change the 
    "isSubmitted" prop to true->false or false->true. Also will update the viewability
    status of the confirmation modal
  */
  handleSubmit(event) {
    this.setState({
      isSubmitted: !this.state.isSubmitted,
      confirmIsOpen: !this.state.confirmIsOpen
    });    
    event.preventDefault();
  }

  /*
    Returns three separate objects with their unique keys. The first object
    is the Device Creation screen itself. This screen contains the fields that
    the user will have to fill in, in order to create a device. It also contains 
    AddDeviceVars component, which contains the "Next" button that will lead the 
    user to the other two objects, the confirmation and sucess modals.
  */
  render() {
    return [
      <div className="container" key="newDeviceScreen">
        <h1>Configure New Device Settings</h1>
        <p className="screenInfo">Please fill in the configuration fields for your new device.</p>

        <form id="createDeviceForm" onSubmit={this.handleNewDeviceCreation}>
          <div className="form-group">
            <input required className="form-control" id="newDeviceNickname" name="newDeviceNickname" placeholder="New Device Nickname" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
            <textarea required className="form-control" id="newDeviceDescription" rows="3" name="newDeviceDescription" placeholder="New Device Description" onChange={this.handleChange}></textarea>
          </div>
          <div className="form-group">
              <select required className="form-control" id="securityQuestion" name="newDeviceType" onChange={this.handleDeviceTypeChange}>
                <option selected disabled hidden value="">Select a Device Type</option>
                <option>ImpinjSpeedwayR420</option>
                <option>ImpinjxArray</option>
              </select>
          </div>

          <div>
            {this.state.showDeviceSpecificSettings ? <AddDeviceVars params={this.state} onFormSubmit={this.handleNewDeviceCreation}></AddDeviceVars> : null}
          </div>

        </form>

        <Link to="/networkManager">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>,

      <Modal show={this.state.confirmIsOpen} key="newDeviceConfirmModal">
        <Modal.Body>
          Is this information for your new device correct?
          <br></br>
          <p>
            <b>Device Nickname:</b> {this.state.newDeviceNickname}
            <br></br>
            <b>Device Description:</b> {this.state.newDeviceDescription}
            <br></br>
            <b>Device Type:</b> {this.state.newDeviceType}
            <br></br>
            <b>Device Name/IP:</b> {this.state.deviceSpecificState.newDeviceName}
            <br></br>
            <b>Device Time:</b> {this.state.deviceSpecificState.newDeviceTime}
            <br></br>
            <b>Device Power:</b> {this.state.deviceSpecificState.newDevicePower}
            <br></br>
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.handleSubmit}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.successIsOpen} key="registerSuccessModal">
        <Modal.Body>Your new device has been created and added to the network!</Modal.Body>
        <Modal.Footer>
          <Link to="/welcome">
            <Button variant="primary" className="float-right">Continue</Button>
          </Link>
        </Modal.Footer>
      </Modal>
      

    ]
  }
}
 
export default AddDeviceHome; 