/*
  The component handles the display of the screen to modify a network's network-specific properties.
*/

import React from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';
import BaseURL from "../utility/BaseURL";

const getNetworkDetailsBaseUrl = BaseURL + 'network';

class ManageNetworkConfiguration extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      originalNetworkName: this.props.location.networkProps["Network Name"],
      originalNetworkProperties: {}, // Filled by componentDidMount()
      newNetworkProperties: {
        "Network Name": "",
        "Network Description": ""
      },
      confirmIsOpen: false,
      successIsOpen: false,
      errorIsOpen: false,
      errorMessage: ""
    }    


    this.toggleConfirmationModal = this.toggleConfirmationModal.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }




  handleChange(event) {
    var updatedNetworkProperties = this.state.newNetworkProperties; // Store from current state
    updatedNetworkProperties[event.target.name] = event.target.value; // Update the json
    
    this.setState({ newNetworkProperties: updatedNetworkProperties }); // Update the state
  }




  toggleConfirmationModal(event) {
    this.setState({ confirmIsOpen: !this.state.confirmIsOpen });
    event.preventDefault();
  }




  // Gets run upon initial component render to load the default values of the text fields
  componentDidMount() {
    fetch(getNetworkDetailsBaseUrl + '?networkName=' + this.state.originalNetworkName)
    .then(res => res.json())
    .then(
      // On success
      (result) => {
        var responseJsonArray = result; // Response is a dictionary 


        var properties = {};
        properties["Network Name"] = responseJsonArray["networkName"];
        properties["Network Description"] = responseJsonArray["description"];


        this.setState({originalNetworkProperties: properties});    
        
        // Initialize all to-be-saved properties to be the original, in the event not all properties are modified so can still be saved
        this.setState({newNetworkProperties: properties});
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




  updateNetworkConfiguration = () => {
    var data = {};


    if (this.state.originalNetworkName === this.state.newNetworkProperties["Network Name"]) {
      data = {
        "networkName": this.state.originalNetworkName,
        "description": this.state.newNetworkProperties["Network Description"]
      }
    }
    else {
      data = {
        "networkName": this.state.originalNetworkName,
        "newNetworkName": this.state.newNetworkProperties["Network Name"],
        "description": this.state.newNetworkProperties["Network Description"]
      }     
    }


    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };


    fetch(getNetworkDetailsBaseUrl, requestOptions)
    .then(
      () => {
        this.setState({ confirmIsOpen: false });
        this.setState({ successIsOpen: !this.state.successIsOpen }); 
      },
      // If put was unsuccessful, update state and display error modal
      (error) => {
        this.setState({ errorIsOpen: !this.state.errorIsOpen }, function () {
          var returnedErrorMessage = error.message;


          this.setState({ errorMessage: returnedErrorMessage }, function () {
            console.log(this.state.errorMessage);


            /*
              Have an error modal for being unable to get network fields. Once button on the error modal is clicked, Chariot goes back to welcome screen
            */ 
          });
        });      
        /*
          Have an error modal for being unable to get network fields. Once button on the error modal is clicked, Chariot goes back to welcome screen
        */ 
      }
    )
  }


  toggleErrorModal = () => {
    this.setState({confirmIsOpen: !this.state.confirmIsOpen});
    this.setState({errorIsOpen: !this.state.errorIsOpen});
  }




  render() {
    return [
      <div className="container" key="modifyNetworkNetworkSpecificSettingsScreen">
        <h1>{this.state.originalNetworkName} - Network Configuration</h1>
        <p className="screenInfo">Modify the network-specific configuration for {this.stateoriginalNetworkName} below, then click 'Save' to confirm the changes.</p>


        <form id="modifyNetworkForm" onSubmit={this.toggleConfirmationModal}>
            <div className="form-group">
              Network Name: <input className="form-control" id="networkNameInput" name="Network Name" defaultValue={this.state.originalNetworkName} onChange={this.handleChange}/>
            </div>
            <div className="form-group">
              Network Description: <textarea className="form-control" id="networkDescriptionInput" rows="5" name="Network Description" defaultValue={this.state.originalNetworkProperties["Network Description"]} onChange={this.handleChange}></textarea>
            </div>
            <Link to="/manageExistingNetworks">
              <Button variant="primary" className="float-left footer-button">Back</Button>
            </Link>
            <Button variant="primary" className="float-right footer-button" type="submit">Save</Button>
        </form>


      </div>,


    <Modal show={this.state.confirmIsOpen} key="modifyNetworkNetworkSpecificSettingsConfirmationModal">
        <ConfirmationModalBody
          confirmationQuestion='Are the network settings displayed below correct?'
          confirmationData = {this.state.newNetworkProperties}
          >
        </ConfirmationModalBody>
        
      <Modal.Footer>
        <Button variant="primary" className="float-left" onClick={this.toggleConfirmationModal}>No</Button>
        <Button variant="primary" className="float-right" onClick={this.updateNetworkConfiguration}>Yes</Button>
      </Modal.Footer>
    </Modal>,


    <Modal show={this.state.successIsOpen} key="modifyNetworkNetworkSpecificSettingsSuccessModal">


      <SuccessModalBody successMessage='The network was succesfully modified! Click "Continue" to go back to the "Network Manager" screen.'>
      </SuccessModalBody>


      <Modal.Footer>
        <Link to="/networkManager">
          <Button variant="primary" className="float-left">Continue</Button>
        </Link>
      </Modal.Footer>
    </Modal>,


    <Modal show={this.state.errorIsOpen && this.state.errorMessage} key="modifyNetworkNetworkSpecificSettingsErrorModal">


      <ErrorModalBody errorMessage={this.state.errorMessage}>
      </ErrorModalBody>


      <Modal.Footer>
        <Button variant="primary" className="float-left" onClick={this.toggleErrorModal}>OK</Button>
      </Modal.Footer>
    </Modal>


    ]
  }
}


export default ManageNetworkConfiguration;