/*
  Register.js

  This component handles the GUI for the registration screen, as well as 
  the modals that appear as the registration process is completed.
*/

import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

import hiddenPasswordImg from "../images/hiddenPassword.PNG";
import showPasswordImg from "../images/showPassword.PNG";

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';

const registerUrl = 'http://localhost:5000/chariot/api/v1.0/register';

class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      accountInfo : {
        "Full Name": "", // Full-name account attribute
        "Username": "", // Username for  attribute
        "Password": "", // Password for account
        "Email Address": "", // Email-address for account
        "Security Question": "", // Security question for account in the event the user forgets their password
        "Security Question Answer": "" // Answer to security question
      },
      securityQuestionOptions : [
        'What was your first pet\'s name?', 
        'What is your dad\'s middle name?',
        'What town or city were you born in?',
        'In what town or city was your first full time job?',
        'What is your favorite sport\'s mascot?'
      ],
      isSubmitted: false, // Whether or not the account information is ready to be sent to the server
      passwordVisible: false, // Whether or not the password is visible on the screen
      passwordImg: hiddenPasswordImg, // Current passwordImg that is shown (hidden/visible)
      confirmIsOpen: false, // Is the confirm modal open?
      successIsOpen: false // Is the success modal open?
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.changePasswordVisibility = this.changePasswordVisibility.bind(this);
  }

  /*
    Updates prop values (account-related) as they are entered by the user.
  */
  handleChange(event) {
    var updatedAccountInfo = this.state.accountInfo; // Store from current state
    updatedAccountInfo[event.target.name] = event.target.value; // Update the json
    
    this.setState({ accountInfo: updatedAccountInfo }); // Update the state
  }

  /* 
    Called when the user either submits the registration form by clicking "Next"
    on the registration screen or "No" on the confirmation modal. Will change the 
    "isSubmitted" prop to true->false or false->true.
  */
  handleSubmit(event) {
    this.setState({
      isSubmitted: !this.state.isSubmitted,
      confirmIsOpen: !this.state.confirmIsOpen
    });    
    event.preventDefault(); // To prevent screen from rerendering
    this.registerUser()
  }

  /*
    Function that launches the success modal after the user confirms the account
    information that they entered is correct. 
    
    Also makes the POST request to the server to create the new account.
  */
  toggleSuccessModal = () => {
    this.setState({
      confirmIsOpen: false
    });
    this.setState({
      successIsOpen: !this.state.successIsOpen
    });
  }


  /*
    Called when the user clicks the button to view/unview the password they entered.
  */
  changePasswordVisibility() {
    if (this.state.passwordImg === hiddenPasswordImg) {
      this.setState({passwordImg: showPasswordImg});
      this.setState({passwordVisible: true});
    } 
    else {
      this.setState({passwordImg: hiddenPasswordImg});
      this.setState({passwordVisible: false});
    }
  }

  registerUser = () => {
    // Post request's body
    var data = {
      "fullName": this.state.accountInfo["Full Name"],
      "username": this.state.accountInfo["Username"],
      "password": this.state.accountInfo["Password"],
      "eMail": this.state.accountInfo["Email Address"]
    }

    // Post request options
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };

    // Execute the post request to 'postCreateNetworkBaseUrl' with 'requestOptions' using fetch
    fetch(registerUrl, requestOptions)
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
  /*
    Returns three separate objects with their unique keys. The first object
    is the Registration screen itself. This screen contains the fields that
    the user will have to fill in, in order to create an account. It also 
    contains the "Next" button that will lead the user to the other two objects,
    the confirmation and sucess modals.
  */
  render() {
    return [
      // Main regsiter element for register component
      <div className="general-component-bg" key="registerForm">
        <div className="container">

          {/* Register screen highlighted via card */}
          <div className="card">
            <div className="card-header">
              <h1>Create an Account</h1>
              <p>To create an account, fill in the required fields, then click "Next."</p>
            </div>

            <div className="card-body">

              {/* When user clicks on button to submit the form, call handleSubmit() to display confirmation modal */}
              <form onSubmit={this.handleSubmit}>
                {/* As fields are typed into, call handleChange() to update and keep track of the values */}
                <div className="form-group">
                  <input required type="text" className="form-control" id="fullname" name="Full Name" placeholder="Full Name" onChange={this.handleChange}/>
                </div>
                
                <div className="form-group">
                  <input required type="text" className="form-control" id="username" name="Username" placeholder="Username" onChange={this.handleChange}/>
                </div>

                {/* Two fields for password and confirm password */}
                <div className="form-group input-group">
                  <input required type={this.state.passwordVisible ? "text" : "password"} className="form-control" id="password" name="Password" placeholder="Password" />
                  <span className="input-group-addon">&nbsp;&nbsp;</span>
                  <input required type={this.state.passwordVisible ? "text" : "password"} className="form-control" id="confirmPassword" name="Password" placeholder="Confirm Password" onChange={this.handleChange}/>
                  <img id="passwordVisibilityImg" src={this.state.passwordImg} alt="Hide/Show Password" onClick={this.changePasswordVisibility}></img>
                </div>

                <div className="form-group">
                  <input required type="email" className="form-control" id="emailAddress" name="Email Address" placeholder="Email Address" onChange={this.handleChange}/>
                  You'll need to verify that this email belongs to you.
                </div>

                <br></br>
                
                {/* Button to submit form for account creation */}
                <Button type="submit" variant="primary" className="float-right" >Next</Button>

                <div className="float-left">
                  Already have a Chariot account? <Link to="/"> Log In</Link>
                </div>

              </form>

            </div>

          </div>

        </div>
      </div>,

      // Confirmation modal element for Register component
      <Modal show={this.state.confirmIsOpen} key="registerConfirmModal">
        <ConfirmationModalBody
          confirmationQuestion='Is this information for your account correct?'
          confirmationData = {this.state.accountInfo}
          >
        </ConfirmationModalBody>
        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.handleSubmit}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Yes</Button>
        </Modal.Footer>
      </Modal>,

      // Sucess modal element for Register component
      <Modal show={this.state.successIsOpen} key="registerSuccessModal">

        <SuccessModalBody successMessage="To complete the account creation process, please check your email to complete the account creation process.">
        </SuccessModalBody>

        <Modal.Footer>
          <Link to="/">
            <Button variant="primary" className="float-right">Continue</Button>
          </Link>
        </Modal.Footer>
      </Modal>

    ]
  }

}


export default Register;