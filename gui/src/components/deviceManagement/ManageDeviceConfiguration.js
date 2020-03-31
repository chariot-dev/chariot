import React from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';

const getDeviceConfigurationBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network/device';
const modifyDeviceConfigurationBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network/device';
const deleteDeviceBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network/device';


class ManageDeviceConfiguration extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // These two state values are used to execute the GET call to get the device's original properties/configuration
      originalDeviceName : this.props.location.networkProps["Device Name"], // this.props.location.deviceProps obtained from prop passed through from Link in ManageExistingNetworks jsx element
      originalNetworkName : this.props.location.networkProps["Network Name"],
      originalDeviceProperties: {}, // Filled by componentDidMount()
      newDeviceProperties: {},
      saveConfirmIsOpen: false,
      saveSuccessIsOpen: false,
      deleteConfirmIsOpen: false,
      deleteSuccessIsOpen: false
    }

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    var updatedDeviceProperties = this.state.newDeviceProperties; // Store from current state
    updatedDeviceProperties[event.target.name] = event.target.value; // Update the json
    
    this.setState({ newDeviceProperties: updatedDeviceProperties }); // Update the state
  }


  // Gets run upon initial component render to load the default values of the text fields  
  componentDidMount() {
   fetch(getDeviceConfigurationBaseUrl + '?networkName=' + this.state.originalNetworkName + '&deviceId=' + this.state.originalDeviceName)
   .then(res => res.json())
   .then(
      // If post was successful, update state and display success modal
      (result) => {
        var responseJsonArray = result; // Response is a dictionary
        
        var properties = {};
        properties["Device Name"] = this.state.originalDeviceName;
        properties["IP Address"] = responseJsonArray["ipAddress"];
        properties["Report Every n Tags"] = responseJsonArray["report_every_n_tags"];
        properties["Session"] = responseJsonArray["session"];
        properties["Start Inventory"] = responseJsonArray["start_inventory"];
        properties["Mode Identifier"] = responseJsonArray["mode_identifier"];
        properties["Tag Population"] = responseJsonArray["tag_population"]; 
        properties["Poll Delay"] = responseJsonArray["pollDelay"];
        properties["Tx Power"] = responseJsonArray["tx_power"];
        properties["Enable Inventory Parameter Spec ID"] = responseJsonArray["EnableInventoryParameterSpecID"];
        properties["Enable ROS Spec ID"] = responseJsonArray["EnableROSpecID"];
        properties["Enable Spec Index"] = responseJsonArray["EnableSpecIndex"]; 

        this.setState({originalDeviceProperties: properties});

        // Initialize all to-be-saved properties to be the original, in the event not all properties are modified so can still be saved
        this.setState({newDeviceProperties: properties});
        console.log(properties);
        console.log(responseJsonArray);
      },
      // On error
      (error) => {
        console.log(error.message);

    
        /*
          Have an error modal for being unable to get device fields. Once button on the error modal is clicked, Chariot goes back to welcome screen
        */ 
      }
   )

  }


  createDeviceConfigurationFields = () => {
    var configurationFields = [];

    for (var key in this.state.originalDeviceProperties) {
      configurationFields.push(
        <div className="form-group">
          {key}: <input className="form-control" id={key} name={key} defaultValue={this.state.originalDeviceProperties[key]} onChange={this.handleChange}/>
        </div>
      ); 
    }

    return configurationFields;
  }


  toggleDeletionConfirmationModal = () => {
    this.setState({deleteConfirmIsOpen: !this.state.deleteConfirmIsOpen});
  }


  toggleModifyConfirmationModal = () => {
    this.setState({saveConfirmIsOpen: !this.state.saveConfirmIsOpen});
  }

  
  modifyDevice = () => {
    var data = {};
    var temp = [this.state.newDeviceProperties['Tag Population']];

    // ======= When creating fields, no reference to field type, so some fields are would be sent as strings when they need to be ints. Also antenna beeds array. Need to fix ========

    if (this.state.originalDeviceName === this.state.newDeviceProperties["Device Name"]) {
      data = {
        "networkName": this.state.originalNetworkName,
        "deviceId": this.state.newDeviceProperties['Device Name'],
        //"newDeviceId": this.state.newDeviceProperties['IP Address'], // Not needed because not changing name
        "ipAddress": this.state.newDeviceProperties['IP Address'],
        "pollDelay": this.state.newDeviceProperties['Poll Delay'],
        "antennas": temp,
        "tag_population": this.state.newDeviceProperties['Tag Population'],
        "report_every_n_tags": this.state.newDeviceProperties['Report Every n Tags'],
        "tx_power": this.state.newDeviceProperties['Tx Power'],
        "session": this.state.newDeviceProperties['Session'],
        "start_inventory": this.state.newDeviceProperties['Start Inventory'],
        "mode_identifier": this.state.newDeviceProperties['Mode Identifier'],
        "EnableROSpecID": this.state.newDeviceProperties['Enable ROS Spec ID'],
        "EnableSpecIndex": this.state.newDeviceProperties['Enable Spec Index'],
        "EnableInventoryParameterSpecID": this.state.newDeviceProperties['Enable Inventory Parameter Spec ID'],
        "EnableRFPhaseAngle": this.state.newDeviceProperties['Enable RF Phase Angle']
      }
    }
    else {
      data = {
        "networkName": this.state.originalNetworkName,
        "deviceId": this.state.originalDeviceName,
        "newDeviceId": this.state.newDeviceProperties['Device Name'], // Needed because changing name
        "ipAddress": this.state.newDeviceProperties['IP Address'],
        "pollDelay": this.state.newDeviceProperties['Poll Delay'],
        "antennas": temp,
        "tag_population": this.state.newDeviceProperties['Tag Population'],
        "report_every_n_tags": this.state.newDeviceProperties['Report Every n Tags'],
        "tx_power": this.state.newDeviceProperties['Tx Power'],
        "session": this.state.newDeviceProperties['Session'],
        "start_inventory": this.state.newDeviceProperties['Start Inventory'],
        "mode_identifier": this.state.newDeviceProperties['Mode Identifier'],
        "EnableROSpecID": this.state.newDeviceProperties['Enable ROS Spec ID'],
        "EnableSpecIndex": this.state.newDeviceProperties['Enable Spec Index'],
        "EnableInventoryParameterSpecID": this.state.newDeviceProperties['Enable Inventory Parameter Spec ID'],
        "EnableRFPhaseAngle": this.state.newDeviceProperties['Enable RF Phase Angle']
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

      
        /*
          Have an error modal for being unable to get network fields. Once button on the error modal is clicked, Chariot goes back to welcome screen
        */ 
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

    
        /*
          Have an error modal for being unable to get network fields. Once button on the error modal is clicked, Chariot goes back to welcome screen
        */ 
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
    console.log(this.state.newDeviceProperties);

    return [
      <div className="container" key="manageDeviceConfigurationScreen">
        <h1>{this.state.originalDeviceName} - Device Configuration</h1>
        <p className="screenInfo">Modifying configuration settings of {this.state.originalDeviceName} for {this.state.originalNetworkName}.</p>

        <form id="modifyDeviceForm">
          {Object.keys(this.state.newDeviceProperties).length === 0 ? null : this.createDeviceConfigurationFields()}
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
        <SuccessModalBody successMessage= {this.state.newDeviceProperties['Device Name'] + ' has successfully been modified.'}>
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