import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';

class DatabaseConnection extends Component {
  constructor(props) {
    super(props);
    this.state = {
      formControls: {
          ipAddress: '',
          name: '',
          password: ''
      },
      
      successMessage : '',
      confirmIsOpen: false,
      successIsOpen: false
    }

    this.testConnection = this.testConnection.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  
  /*
    Updates prop values (account-related) as they are entered by the user.
  */
  handleChange(event) {
    var updatedFormControls = this.state.formControls; // Store from current state
    updatedFormControls[event.target.name] = event.target.value; // Update the json
    
    this.setState({ formControls: updatedFormControls }); // Update the state
  }

  toggleConfirmationModal = () => {
    this.setState({
      confirmIsOpen: !this.state.confirmIsOpen
    });
  }

  /*
    Currently using the handleSubmit method to try to establish a TCP connection with a database
    if the connection is successful, then show success message. Otherwise, show failure message and do
    not proceed to next screen
  */
  testConnection(event) {
    //currently assuming that connection will always be established, display that connection is successful for 3 seconds
    setTimeout(() => this.setState({ message: 'Connection Successful!' }), 3000);
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
      <div className="container" key="databaseConnectionScreen">
        <h1>Database Connection</h1>
        <p className="screenInfo">Please fill in the following fields to connect to the database that will store the data.</p>

        <form>
          <div className="form-group">
            <input required type="text" className="form-control" id="ipAddress" name="ipAddress" placeholder="IP Address" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
            <input required type="text" className="form-control" id="name" name="name" placeholder="Name" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
            <input required type="password" className="form-control" id="password" name="password" placeholder="Password" onChange={this.handleChange}/>
          </div>         

        </form>

        <Link to="/chooseNetwork">
            <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
        <Button variant="primary" className="float-right footer-button" onClick={this.toggleConfirmationModal}>Connect</Button>
      </div>,

      <Modal show={this.state.confirmIsOpen} key="databaseConnectionConfirmModal">

        <ConfirmationModalBody
          confirmationQuestion= 'If the information below about your database is correct, please click "Confirm".'
          confirmationData = ''
          >
        </ConfirmationModalBody>

      <Modal.Footer>
        <Button variant="primary" className="float-left" onClick={this.handleSubmit}>No</Button>
        <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Confirm</Button>
      </Modal.Footer>
    </Modal>,

    <Modal show={this.state.successIsOpen} key="databaseConnectionSuccessModal">

      <SuccessModalBody successMessage='Successfully connected to your database. To begin your data collection episode, please click "Continue"'>
      </SuccessModalBody>

      <Modal.Footer>
        <Link to='/dataCollectionEpisodeStatus'>
          <Button variant="primary" className="float-right">Continue</Button>
        </Link>
      </Modal.Footer>
    </Modal>


    ]
  }




}

export default DatabaseConnection;