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
import BaseURL from "../utility/BaseURL";

const getSupportedDeviceTypesBaseUrl = BaseURL;
const getDeviceConfigBaseUrl = BaseURL + 'network/device/config';
const postDeviceCreationBaseUrl = BaseURL + "network/device";

class AddDeviceHome extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newDeviceTypeGeneralVals: {
        newDeviceTypeConfig: null
      },
      supportedDeviceTypes: [],
      showDeviceSpecificSettings: false, // Whether or not the type of device has been chosen by the user already
      isSubmitted: false, // Whether or not the device information is ready to be sent to the server
      confirmIsOpen: false, // Is the confirm modal open?
      successIsOpen: false, // Is the success modal open?
      errorIsOpen: false, // Is the error modal open?
      errorMessage: '', // Error messagae to be displayed, if necessary
      deviceState: {} // All configuration setting values for the device (From AddDeviceHome and AddDeviceVars)
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleDeviceTypeChange = this.handleDeviceTypeChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  // Gets supported device types when page initially loads in order to dynamically fill in select-menu
  componentDidMount() {
    fetch(getSupportedDeviceTypesBaseUrl + "network/device/supportedDevices")
    .then(res => res.json())
    .then(
      // On success
      (result) => {
        var tempSupportedDeviceTypes = [];
        for (var key in result) {
          tempSupportedDeviceTypes.push(key);
        }
        this.setState({supportedDeviceTypes: tempSupportedDeviceTypes});
      },
      // On error
      (error) => {
        console.log(error.message);
      }
    )
  }

  getSupportedDeviceTypeOptions = () => {
    var deviceOptionsElement = [];

    for (var k = 0; k < this.state.supportedDeviceTypes.length; k++) {
      deviceOptionsElement.push(<option>{this.state.supportedDeviceTypes[k]}</option>);
    }

    return deviceOptionsElement;
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
    var lastDeviceType = this.state.newDeviceTypeGeneralVals['Device Type'];

    if (lastDeviceType !== event.target.value) { // If device type was changed
      var updatedNewDeviceTypeGeneralVals = this.state.newDeviceTypeGeneralVals; // Store from current state
      updatedNewDeviceTypeGeneralVals[event.target.name] = event.target.value; // Update the json with the new device type

      // State is update asynchronousyly, so run function after state is updated
      this.setState({ newDeviceTypeGeneralVals: updatedNewDeviceTypeGeneralVals }, function () {
        // Execute the post request to 'postCreateNetworkBaseUrl' with 'requestOptions' using fetch
        fetch(getDeviceConfigBaseUrl + "?deviceId=" + this.state.newDeviceTypeGeneralVals['Device Type'])
        .then(res => res.json())
        .then(
          // If post was successful, update state and display success modal
          (result) => {
            var responseJson = result;
            updatedNewDeviceTypeGeneralVals['newDeviceTypeConfig'] = responseJson;

            // Store the device's config file to the state
            this.setState({newDeviceTypeGeneralVals: updatedNewDeviceTypeGeneralVals});
            this.setState({showDeviceSpecificSettings: true}); // Will cause render to update device-specific section
          },
          // If post was unsuccessful, update state and display error modal
          (error) => {
            console.log(error.message);
          }
        )

        this.setState({ showDeviceSpecificSettings: false}); // Reset to false after render to get ready for next render (if user changes device type)
      });
    }
  }

  handleNewDeviceCreation = (submittedDeviceSpecificState) => {
    this.setState ({ deviceState: submittedDeviceSpecificState }, () => {
      // Update state to launch confirmation modal
      this.setState({
        isSubmitted: !this.state.isSubmitted,
        confirmIsOpen: !this.state.confirmIsOpen
      });
    });
  }

  /*
    Function that launches the success modal after the user confirms the device
    information that they entered is correct. Also makes the POST request to the
    server to create the new device.
  */
 toggleSuccessModal = () => {
    var data = {};
    data["networkName"] = this.props.location.networkProps["Network Name"];
    data["deviceType"] = this.state.deviceState.newDeviceTypeGeneralVals['Device Type'];

    for (var key in this.state.deviceState.newDeviceTypeConfigVals) {
      var fieldVal = this.state.deviceState.newDeviceTypeConfigVals[key].value;

      //only add to data if the value is not empty
      if (fieldVal !== "") {
        var curFieldId = this.state.deviceState.newDeviceTypeConfigVals[key].alias;
        var fieldType = this.state.deviceState.newDeviceTypeConfigVals[key].inputType;

        if (fieldType === "number") {
            fieldVal = parseInt(fieldVal)
        }
        else if (fieldType === "checkbox") {
            fieldVal = document.getElementById(curFieldId).checked;
        }
        else if (fieldType === "numberArray") {
            var inputValues = fieldVal.split(" ");

            //again need to verify that all values will be ints
            var arr = [];

            inputValues.forEach(function (item) {
                arr.push(parseInt(item))
            });

            fieldVal = arr;
        }

        data[curFieldId] = fieldVal;
      }
    }

    // Post request options
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };

    // Execute the post request to 'postCreateNetworkBaseUrl' with 'requestOptions' using fetch
    fetch(postDeviceCreationBaseUrl, requestOptions)
    .then(res => res.json())
    .then(
      // If post was successful, update state and display success modal
      () => {
      this.setState({
        confirmIsOpen: false
      });
      this.setState({
        successIsOpen: !this.state.successIsOpen
      });
      },
      // If post was unsuccessful, update state and display error modal
      (error) => {
      // Once error message is set, then launch the error modal
      this.setState({
        errorMessage: error.message
      }, () => {
        this.setState({ errorIsOpen: !this.state.errorIsOpen });
      });
      }
    )
  }


  toggleErrorModal = () => {
    this.setState({ confirmIsOpen: false });
    this.setState({ errorIsOpen: !this.state.errorIsOpen });
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
              <select required className="form-control" id="Device Type Select" name="Device Type" onChange={this.handleDeviceTypeChange}>
                <option selected disabled hidden value="">Select a Device Type</option>
                {this.getSupportedDeviceTypeOptions()}
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

        <ErrorModalBody errorMessage={this.state.errorMessage + ". Please go back, verify that the information is correct, and then try again."}>
        </ErrorModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.toggleErrorModal}>OK</Button>
        </Modal.Footer>
      </Modal>
    ]
  }
}

export default AddDeviceHome;
