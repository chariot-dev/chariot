/*
  The component that handles the functinality for deleting a network. The body of the screen (network/device info)
  is generated through NetworkDeviceCellScreenTemplate as the child component, and uses a callback to update this
  component's state. deleteNetwork={this.deleteConfirmation.bind(this)} is passed as a callback to
  NetworkDeviceCellScreenTemplate. When the 'Delete Network' is pressed in the child (NetworkDeviceCellScreenTemplate),
  it calls this.props.deleteNetwork.bind(this, curNetworkName), which in turn, calls deleteConfirmation(selectedNetwork)
  in the parent (this component).
*/

import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import NetworkDeviceCellScreenTemplate from '../shared/NetworkDeviceCellScreenTemplate';

import SuccessModalBody from '../shared/SuccessModalBody';
import BaseURL from "../utility/BaseURL";

const getAllNetworksBaseUrl = BaseURL + 'networks/all';
const deleteNetworkBaseUrl = BaseURL + 'network';

class DeleteNetwork extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingNetworks: [],
      confirmIsOpen: false,
      selectedNetworkToDelete: null,
      successIsOpen: false
    }


    this.hideConfirmationModal = this.hideConfirmationModal.bind(this);
  } 


  componentDidMount() {
    fetch(getAllNetworksBaseUrl)
    .then(res => res.json())
    .then(
      // On success
      (result) => {
        var responseJsonArray = result; // Response is a dictionary  


        var updatedNetworksJsonArray = this.state.existingNetworks;


        for (var i = 0; i < responseJsonArray.length; i++) {
          updatedNetworksJsonArray.push(responseJsonArray[i]);
        }


        this.setState({ existingNetworks: updatedNetworksJsonArray });
      },
      // On error
      (error) => {
        console.log(error.message);


  
        /*
          Have an error modal for being unable to get device types. Once button on the modal is clicked, Chariot goes back to welcome screen
        */ 
      }
    )
  }




  deleteConfirmation(selectedNetwork) {
    this.setState({confirmIsOpen: true});
    this.setState({selectedNetworkToDelete: selectedNetwork});
    console.log(selectedNetwork)
  }




  hideConfirmationModal(event) {
    this.setState({
      confirmIsOpen: !this.state.confirmIsOpen
    });    
    event.preventDefault();
  }




  toggleSuccessModal = () => {
    // Delete request options
    const requestOptions = {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    };


    fetch(deleteNetworkBaseUrl + "?networkName=" + this.state.selectedNetworkToDelete, requestOptions)
    // On success
    .then(
      () => {
        this.setState({
          confirmIsOpen: false
        });
        this.setState({
          successIsOpen: !this.state.successIsOpen
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




  render() {
    return [
      <div className="container" key="deleteNetworkScreen">
        <h1>Delete an Existing Network</h1>
        <p className="screenInfo">
          Select a network to delete. Deleting a network will also delete its corresponding devices.
        </p>


        {/* {this.state.existingNetworkNames ? this.createNetworkLinks() : null} */}


        {this.state.existingNetworks ? <NetworkDeviceCellScreenTemplate dataJson={this.state.existingNetworks} withLinks={false} type="delete" deleteNetwork={this.deleteConfirmation.bind(this)}></NetworkDeviceCellScreenTemplate> : null}
        
        <Link to="/networkManager">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
      </div>,


      <Modal show={this.state.confirmIsOpen} key="networkDeletionConfirmModal">
        <Modal.Body>
          To confirm the deletion of the network, {this.state.selectedNetworkToDelete}, click 'Yes'.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.hideConfirmationModal}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Yes</Button>
        </Modal.Footer>
      </Modal>,


      <Modal show={this.state.successIsOpen} key="networkDeletionSuccessModal">


        <SuccessModalBody successMessage="The network has been deleted!">
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


export default DeleteNetwork;