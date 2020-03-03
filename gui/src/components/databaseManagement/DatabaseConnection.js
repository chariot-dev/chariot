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

    console.log(this.props.location.networkProps['Network Name'])
    this.state = {
      chosenNetwork: this.props.location.networkProps['Network Name'],
      formControls: {
          "IP Address": '',
          "Name": '',
          "Password": ''
      },
      
      successMessage : '',
      confirmIsOpen: false,
      successIsOpen: false
    }

    this.testConnection = this.testConnection.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleCancelConfirmation = this.handleCancelConfirmation.bind(this);
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


  handleCancelConfirmation(event) {
    this.setState({
      isSubmitted: !this.state.isSubmitted,
      confirmIsOpen: !this.state.confirmIsOpen
    });    
    event.preventDefault(); // To prevent screen from rerendering
  }


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

        <form onSubmit={this.toggleConfirmationModal}>
          <div className="form-group">
            <input required type="text" className="form-control" id="ipAddress" name="ipAddress" placeholder="IP Address" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
            <input required type="text" className="form-control" id="name" name="name" placeholder="Name" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
            <input required type="password" className="form-control" id="password" name="password" placeholder="Password" onChange={this.handleChange}/>
          </div>         
          <Link to="/chooseNetwork">
            <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>

        <Button variant="success" className="footer-button button-mid-bottom">Test Connection</Button>

        <Button variant="primary" className="float-right footer-button" type="submit">Connect</Button>

        </form>


      </div>,

      <Modal show={this.state.confirmIsOpen} key="databaseConnectionConfirmModal">

        <ConfirmationModalBody
          confirmationQuestion= 'If the information below about your database is correct, please click "Confirm".'
          confirmationData = {this.state.formControls}
          >
        </ConfirmationModalBody>

      <Modal.Footer>
        <Button variant="primary" className="float-left" onClick={this.handleCancelConfirmation}>No</Button>
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