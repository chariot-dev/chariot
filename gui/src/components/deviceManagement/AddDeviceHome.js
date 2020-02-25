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

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';

const getDeviceConfigBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network/device/config';
const postDeviceCreationBaseUrl = "http://localhost:5000/chariot/api/v1.0/network/device";
const xhr = new XMLHttpRequest();

class AddDeviceHome extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newDeviceTypeGeneralVals: {
        'Device Nickname': null,
        'Device Description': null,
        'Device Type': null,
        newDeviceTypeConfig: null
      },
      showDeviceSpecificSettings: false, // Whether or not the type of device has been chosen by the user already
      isSubmitted: false, // Whether or not the device information is ready to be sent to the server
      confirmIsOpen: false, // Is the confirm modal open?
      successIsOpen: false, // Is the success modal open?
      errorIsOpen: false, // Is the error modal open?
      deviceState: {} // All configuration setting values for the device (From AddDeviceHome and AddDeviceVars)
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleDeviceTypeChange = this.handleDeviceTypeChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  /*
    Updates textfield state values as they are entered by the user.
  */  
  handleChange(event) {
    var updatedNewDeviceTypeGeneralVals = this.state.newDeviceTypeGeneralVals; // Store from current state
    updatedNewDeviceTypeGeneralVals[event.target.name] = event.target.value; // Update the json
    
    this.setState({ newDeviceTypeGeneralVals: updatedNewDeviceTypeGeneralVals }); // Update the state
  }


  /*
    As the device type the user selects changes, update that in the state.
  */
  handleDeviceTypeChange(event) {
    console.log("------------------- changed -------------------");
    var lastDeviceType = this.state.newDeviceTypeGeneralVals['Device Type'];
    
    if (lastDeviceType !== event.target.value) {
      var updatedNewDeviceTypeGeneralVals = this.state.newDeviceTypeGeneralVals; // Store from current state
      updatedNewDeviceTypeGeneralVals[event.target.name] = event.target.value; // Update the json with the new device type

      // State is update asynchronousyly, so run function after state is updated
      this.setState({ newDeviceTypeGeneralVals: updatedNewDeviceTypeGeneralVals }, function () {
        console.log(this.state.newDeviceTypeGeneralVals);

        xhr.open('GET', getDeviceConfigBaseUrl + "?DeviceName=" + this.state.newDeviceTypeGeneralVals['Device Type']);
        xhr.setRequestHeader('Content-Type', 'application/json');
        
        // Once a response is received
        xhr.onreadystatechange = () => {
          if (xhr.readyState === XMLHttpRequest.DONE) { // Once the request is done
              var responseJson = JSON.parse(xhr.response);

              console.log(responseJson);

              console.log(updatedNewDeviceTypeGeneralVals);

              updatedNewDeviceTypeGeneralVals['newDeviceTypeConfig'] = responseJson;

              console.log(updatedNewDeviceTypeGeneralVals);

              // Store the device's config file to the state
              this.setState({newDeviceTypeGeneralVals: updatedNewDeviceTypeGeneralVals});
              this.setState({showDeviceSpecificSettings: true}); // Will cause render to update device-specific section
          }
        }

        xhr.send(); // Send the request to the url with set headers

        this.setState({ showDeviceSpecificSettings: false}); // Reset to false after render to get ready for next render
      });
    }
  }

  handleNewDeviceCreation = (submittedDeviceSpecificState) => {
    console.log(submittedDeviceSpecificState);
    this.setState ({ deviceState: submittedDeviceSpecificState }, () => {
      console.log(this.state.deviceState);
    });

    

    /*
    var temp = [];
    for (var key in submittedDeviceSpecificState) {
      temp.push(submittedDeviceSpecificState[key]);
    }
    this.setState ({ deviceState: temp }, () => {
      console.log(this.state.deviceState);
    });
    */
    // Update state to launch confirmation modal
    this.setState({
      isSubmitted: !this.state.isSubmitted,
      confirmIsOpen: !this.state.confirmIsOpen
    }); 
  }


  /*
    Function that launches the success modal after the user confirms the device
    information that they entered is correct. Also makes the POST request to the
    server to create the new device.
  */
 toggleSuccessModal = () => {
    xhr.open('POST', postDeviceCreationBaseUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = () => {// Call a function when the state changes.
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          this.setState({ confirmIsOpen: false });
          this.setState({ successIsOpen: !this.state.successIsOpen });
        }
      }
    }    
    
    // ============================== FIX LATER. SHOULDN'T HAVE TO HAVE CONDITIONAL ==============================
    var data = {};

    console.log(this.props.location.networkProps);
    console.log(this.state.deviceState.newDeviceTypeConfigVals);

    data["NetworkName"] = this.props.location.networkProps['Network Name'];
    data["deviceId"] = this.state.deviceState.newDeviceTypeGeneralVals['Device Nickname'];
    data["deviceType"] = this.state.deviceState.newDeviceTypeGeneralVals['Device Type'];
    data["pollDelay"] = "xxxxxxxx";

    for (var key in this.state.deviceState.newDeviceTypeConfigVals) {
      console.log(key);
      console.log(this.state.deviceState.newDeviceTypeConfigVals[key]);

      data[this.state.deviceState.newDeviceTypeConfigVals[key].alias] = this.state.deviceState.newDeviceTypeConfigVals[key].value;
    }

    xhr.send(JSON.stringify(data));
  }

  toggleErrorModal = () => {
    this.setState({
      confirmIsOpen: false
    });
    this.setState({
      errorIsOpen: !this.state.errorIsOpen
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


  parseConfirmationData = () => {
    var confirmationDataJson = {};

    confirmationDataJson['Device Nickname'] = this.state.newDeviceTypeGeneralVals['Device Nickname'];
    confirmationDataJson['Device Description'] = this.state.newDeviceTypeGeneralVals['Device Description'];
    confirmationDataJson['Device Type'] = this.state.newDeviceTypeGeneralVals['Device Type'];

    for (var key in this.state.deviceState.newDeviceTypeConfigVals) {
      confirmationDataJson[key] = this.state.deviceState.newDeviceTypeConfigVals[key].value;
    }

    return confirmationDataJson;
  }
  

  /*
    Returns three separate objects with their unique keys. The first object
    is the Device Creation screen itself. This screen contains the fields that
    the user will have to fill in, in order to create a device. It also contains 
    AddDeviceVars component, which contains the "Next" button that will lead the 
    user to the other two objects, the confirmation and sucess modals.
  */
  render() {
    // If config for device type (e.g. Impinjxarray) was obtained, load the form with the device-specific section
    return [
      <div className="container" key="newDeviceScreen">
        <h1>Configure New Device Settings</h1>
        <p className="screenInfo">Please fill in the configuration fields for your new device.</p>

        <form id="createDeviceForm">
          <div className="form-group">
            <input required className="form-control" id="Device Nickname" name="Device Nickname" placeholder="Device Nickname" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
            <textarea required className="form-control" id="Device Description" rows="3" name="Device Description" placeholder="Device Description" onChange={this.handleChange}></textarea>
          </div>
          <div className="form-group">
              <select required className="form-control" id="securityQuestion" name="Device Type" onChange={this.handleDeviceTypeChange}>
                <option selected disabled hidden value="">Select a Device Type</option>
                <option>ImpinjSpeedwayR420</option>
                <option>ImpinjxArray</option>
              </select>
          </div>

            {/* onFormSubmit() callback. Pass in as prop basically. */}
            {this.state.showDeviceSpecificSettings ? <AddDeviceVars params={this.state} onFormSubmit={this.handleNewDeviceCreation}></AddDeviceVars> : null}
        </form>

        <Link to="/networkManager">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>,

      <Modal show={this.state.confirmIsOpen} key="newDeviceConfirmModal">
        
        <ConfirmationModalBody
          confirmationQuestion={('Before ').concat(this.state.newDeviceTypeGeneralVals['Device Nickname'], ' is added to ', this.props.location.networkProps['Network Name'], ' please confirm that the information below is correct.')} 
          confirmationData = {this.parseConfirmationData()}
          >
        </ConfirmationModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.handleSubmit}>Incorrect</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Correct</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.successIsOpen} key="registerSuccessModal">
        <SuccessModalBody successMessage="Your new device has been created and added to the network!">
        </SuccessModalBody>
        <Modal.Footer>
          <Link to="/welcome">
            <Button variant="primary" className="float-right">Continue</Button>
          </Link>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.errorIsOpen} key="addDeviceErrorModal">

        <ErrorModalBody errorMessage="Your device was not added to the network. Please go back, verify that the information is correct, and then try again.">
        </ErrorModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.toggleErrorModal}>OK</Button>
        </Modal.Footer>
      </Modal>
    ]
  }
}
 
export default AddDeviceHome; 