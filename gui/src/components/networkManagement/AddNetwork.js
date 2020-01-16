import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

class AddNetwork extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newNetworkName: "",
      newNetworkDescription: "",
      isSubmitted: false,
      confirmIsOpen: false,
      successIsOpen: false
    }

    this.handleNetworkAdd = this.handleNetworkAdd.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleNetworkAdd(event) {
    this.setState({ isSubmitted: true });
    event.preventDefault();
  }
  
  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  toggleConfirmationModal = () => {
    this.setState({
      confirmIsOpen: !this.state.confirmIsOpen
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

  render() {
    return [
      <div className="container" key="addNetworkForm">
        <h1>Add a New Network</h1>
          <p className="screenInfo">Please fill in the fields below to create a network. Then, click "Next".</p>
          
          <form id="createNetworkForm" onSubmit={this.handleNetworkAdd}>
            <div className="form-group">
              <input className="form-control" id="networkNameInput" name="newNetworkName" placeholder="New Network Name" onChange={this.handleChange}/>
            </div>
            <div className="form-group">
              <textarea className="form-control" id="networkDescriptionInput" rows="5" name="newNetworkDescription" placeholder="New Network Description" onChange={this.handleChange}></textarea>
            </div>
            <Link to="/networkManager">
              <Button variant="primary" className="float-left footer-button">Back</Button>
            </Link>
            <Button variant="primary" className="float-right footer-button" onClick={this.toggleConfirmationModal}>Next</Button>
        </form>
      </div>,

      <Modal show={this.state.confirmIsOpen} key="addNetworkConfirmation">
        <Modal.Body>
          Is this information for your network correct?
          <br></br>
          <b>Name:</b> {this.state.newNetworkName}
          <br></br>
          <b>Description:</b> {this.state.newNetworkDescription}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.toggleConfirmationModal}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      <Modal show={this.state.successIsOpen} key="addNetworkSuccessModal">
        <Modal.Body>Your network was succesfully added! Would you like to add a device to this network as well?</Modal.Body>
        <Modal.Footer>
          <Link to="/networkManager">
            <Button variant="primary" className="float-left">No</Button>
          </Link>
          <Link to="/addDeviceHome">
            <Button variant="primary" className="float-right">Yes</Button>
          </Link>
        </Modal.Footer>
      </Modal>
    ]
  }

}

export default AddNetwork; 