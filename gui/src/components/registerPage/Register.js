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

class Register extends Component {
  constructor(props) {
    super(props);
    this.state = {
      fullname: "", // Full-name account attribute
      username: "", // Username for  attribute
      password: "", // Password for account
      emailAddress: "", // Email-address for account
      securityQuestion: "", // Security question for account in the event the user forgets their password
      securityQuestionAnswer: "", // Answer to security question
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
    this.setState({[event.target.name]: event.target.value});
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
  
  componentDidMount() {
    fetch("https://api.example.com/items")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            items: result.items
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  /*
    Called when the user clicks the button to view/unview the password they entered.
  */
  changePasswordVisibility() {
    console.log(this.state.passwordImg);

    if (this.state.passwordImg === hiddenPasswordImg) {
      this.setState({passwordImg: showPasswordImg});
      this.setState({passwordVisible: true});
    } 
    else {
      this.setState({passwordImg: hiddenPasswordImg});
      this.setState({passwordVisible: false});
    }

    console.log(this.state.passwordImg);
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
                  <input required type="text" className="form-control" id="fullname" name="fullname" placeholder="Full Name" onChange={this.handleChange}/>
                </div>
                
                <div className="form-group">
                  <input required type="text" className="form-control" id="username" name="username" placeholder="Username" onChange={this.handleChange}/>
                </div>

                {/* Two fields for password and confirm password */}
                <div className="form-group input-group">
                    <input required type={this.state.passwordVisible ? "text" : "password"} className="form-control" id="password" name="password" placeholder="Password" />
                    <span className="input-group-addon">&nbsp;&nbsp;</span>
                    <input required type={this.state.passwordVisible ? "text" : "password"} className="form-control" id="confirmPassword" name="password" placeholder="Confirm Password" onChange={this.handleChange}/>
                    <img id="passwordVisibilityImg" src={this.state.passwordImg} alt="Hide/Show Password" onClick={this.changePasswordVisibility}></img>
                </div>

                <div className="form-group">
                    <input required type="email" className="form-control" id="emailAddress" name="emailAddress" placeholder="Email Address" onChange={this.handleChange}/>
                    You'll need to verify that this email belongs to you.
                </div>

                <div className="form-group">
                    <select required className="form-control" id="securityQuestion" name="securityQuestion" onChange={this.handleChange}>
                      <option selected disabled hidden value="">Select a Security Question</option>
                      <option>What was your first pet's name?</option>
                      <option>What is your dad's middle name?</option>
                      <option>What city were you born in?</option>
                      <option>What is your favorite sport's mascot?</option>
                    </select>
                </div>

                <div className="form-group">
                    <input required type="text" className="form-control" id="securityQuestionAnswer" name="securityQuestionAnswer" placeholder="Security Question Answer" onChange={this.handleChange}/>
                </div>

                <br></br>
                
                {/* Button to submit form for account creation */}
                <Button type="submit" variant="primary" className="float-right">Next</Button>

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

        <Modal.Body>
          Is this information for your account correct?
          <br></br>
          <p>
            <b>Name:</b> {this.state.fullname}
            <br></br>
            <b>Username:</b> {this.state.username}
            <br></br>
            <b>Password:</b> {this.state.password}
            <br></br>
            <b>Email Address:</b> {this.state.emailAddress}
            <br></br>
            <b>Security Question:</b> {this.state.securityQuestion}
            <br></br>
            <b>Security Question Answer:</b> {this.state.securityQuestionAnswer}
          </p>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.handleSubmit}>No</Button>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>Yes</Button>
        </Modal.Footer>

      </Modal>,

      // Sucess modal element for Register component
      <Modal show={this.state.successIsOpen} key="registerSuccessModal">

        <Modal.Body>To complete the account creation process, please check your email to complete the account creation process.</Modal.Body>

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