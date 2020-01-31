import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import AddDeviceVars from './AddDeviceVars'

// Figure out whether multiple device additions in one-go should be a thing

class AddDeviceHome extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newDeviceNickname: "",
      newDeviceDescription: "",
      newDeviceType: "",
      showDeviceSpecificSettings: false,
      isSubmitted: false,
      confirmIsOpen: false,
      successIsOpen: false,
      deviceSpecificState: {},
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
  
  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  handleDeviceTypeChange(event) {
    // Update chosen device type
    this.setState({[event.target.name]: event.target.value});

    // Boolean to show the device type's-specific settings to true
    this.setState({
      showDeviceSpecificSettings: true
    });
  }

  toggleSuccessModal = () => {
    this.setState({
      confirmIsOpen: false
    });
    this.setState({
      successIsOpen: !this.state.successIsOpen
    });
  }

  handleSubmit(event) {
    this.setState({
      isSubmitted: !this.state.isSubmitted,
      confirmIsOpen: !this.state.confirmIsOpen
    });    
    event.preventDefault();
  }

  render() {
    return [
      <div className="container" key="newDeviceScreen">
        <h1>Configure New Device Settings</h1>
        <p className="screenInfo">Please fill in the fields for your new device.</p>

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
                <option>R420</option>
                <option>X-Array</option>
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