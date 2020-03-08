import React from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

//import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';

var getDeviceConfigurationBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network/device';
const deleteDeviceBaseUrl = 'http://localhost:5000/chariot/api/v1.0/network/device';
const xhr = new XMLHttpRequest();

class ManageDeviceConfiguration extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      // These two state values are used to execute the GET call to get the device's original properties/configuration
      originalDeviceName : this.props.location.networkProps["Device Name"], // this.props.location.deviceProps obtained from prop passed through from Link in ManageExistingNetworks jsx element
      originalNetworkName : this.props.location.networkProps["Network Name"],
      originalDeviceProperties: {}, // Filled by componentDidMount()
      newDeviceProperties: {},
      confirmIsOpen: false,
      successIsOpen: false,
      deleteIsOpen: false
    }
  }


  // Gets run upon initial component render to load the default values of the text fields  
  componentDidMount() {
    xhr.open('GET', getDeviceConfigurationBaseUrl + '?networkName=' + this.state.originalNetworkName + '&deviceId=' + this.state.originalDeviceName);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Once a response is received
    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status === 200) {
          console.log(xhr.response);
          var responseJsonArray = JSON.parse(xhr.response); // Response is a dictionary 

          var properties = {};
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
        }
      }
    }
    
    xhr.send();
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

  toggleDeletionModal = () => {
    console.log('hi')
    this.setState({deleteIsOpen: !this.state.deleteIsOpen});
  }

  toggleSuccessModal = () => {
    xhr.open('DELETE', deleteDeviceBaseUrl + "?networkName=" + this.state.originalNetworkName + "&deviceId=" + this.state.originalDeviceName);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) { // Once the request is done
        if (xhr.status === 200) {
          this.setState({
            confirmIsOpen: false
          });
          this.setState({
            successIsOpen: !this.state.successIsOpen
          });    
        }
        else {
          console.log("ERROR");
        }  
      }
    }

    xhr.send();
  }


  render() {
    console.log(this.state.originalDeviceName + "   " + this.state.originalNetworkName);

    return [
      <div className="container" key="manageDeviceConfigurationScreen">
        <h1>{this.state.originalDeviceName} - Device Configuration</h1>
        <p className="screenInfo">Modifying configuration settings of {this.state.originalDeviceName} for {this.state.originalNetworkName}.</p>

        <form id="modifyDeviceForm" onSubmit={this.toggleConfirmationModal}>
          {Object.keys(this.state.newDeviceProperties).length === 0 ? null : this.createDeviceConfigurationFields()}
        </form>

        <Link to="/manageExistingNetworks">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>

        <Button variant="danger" className="footer-button button-mid-bottom" onClick={this.toggleDeletionModal}>Delete Device</Button>

        <Button variant="success" className="float-right footer-button">Save</Button>
      </div>,

      <Modal show={this.state.deleteIsOpen} key="deviceDeletionConfirmModal">
        <Modal.Body>
          To confirm the deletion of the device, {this.state.originalDeviceName}, click 'Yes'.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.handleSubmit}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.successIsOpen} key="deviceDeletionSuccessModal">
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