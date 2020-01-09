import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import SuccessModal from '../shared/SuccessModal';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

class AddNetworkConfirm extends Component {
  constructor(props) {
    super(props);

    this.state = { isOpen: false };

    this.toggleModal = this.toggleModal.bind(this);
  }

  toggleModal = () => {
    this.setState({
      isOpen: !this.state.isOpen
    });
  }

  render() {
    /*
    if (this.state.isOpen) {
      return (
      <SuccessModal show={this.state.isOpen}
        onClose={this.toggleModal}>
        Here's some content for the modal
      </SuccessModal> 
      );
    }
    */

    return [
      <div className="container" key="one">
        <h1>Add a New Network</h1>
        <p>Please confirm that the information about the network is correct, then click "Create Network".</p>
        <br></br>

        <b>Name:</b>
        <br></br>
        <b>Description:</b>
        <br></br>
        <br></br>
        <br></br>
        
        <Link to="/addNetwork">
          <button className="btn btn-primary float-left">Back</button>
        </Link>   
        <button className="btn btn-primary float-right" onClick={this.toggleModal}>Create Network</button>
      </div>,

      <Modal show={this.state.isOpen} key="two">
        <Modal.Body>Your network was succesfully added!</Modal.Body>
        <Link to="/networkManager">
          <Button variant="primary" className="float-right">Continue</Button>
        </Link>
      </Modal>
     

    ]
  }

}
  
export default AddNetworkConfirm; 