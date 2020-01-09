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
    console.log("Submitted");
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
          <p>Please fill in the fields below to create a network. Then, click "Next".</p>
          <br></br>
          
          <form id="createNetworkForm" onSubmit={this.handleNetworkAdd}>
            <div className="form-group">
              <input className="form-control" id="networkNameInput" name="newNetworkName" placeholder="Name" onChange={this.handleChange}/>
            </div>
            <div className="form-group">
              <textarea className="form-control" id="networkDescriptionInput" rows="5" name="newNetworkDescription" placeholder="Description" onChange={this.handleChange}></textarea>
            </div>
            <Link to="/networkManager">
              <Button variant="primary" className="float-left">Back</Button>
            </Link>
            <Button variant="primary" className="float-right" onClick={this.toggleConfirmationModal}>Next</Button>
        </form>
      </div>,

      <Modal show={this.state.confirmIsOpen} key="addNetworkConfirmation">
        <Modal.Body>
          Is this information for your network correct?
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
        <Modal.Body>Your network was succesfully added!</Modal.Body>
        <Link to="/networkManager">
          <Button variant="primary" className="float-right">Continue</Button>
        </Link>
      </Modal>
    ]
  }

}

export default AddNetwork; 