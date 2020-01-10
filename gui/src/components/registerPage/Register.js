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
      fullname: "",
      username: "",
      password: "",
      emailAddress: "",
      securityQuestion: "",
      securityQuestionAnswer: "",
      isSubmitted: false,
      passwordVisible: false,
      passwordImg: hiddenPasswordImg,
      confirmIsOpen: false,
      successIsOpen: false
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.changePasswordVisibility = this.changePasswordVisibility.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  handleSubmit(event) {
    this.setState({
      isSubmitted: !this.state.isSubmitted,
      confirmIsOpen: !this.state.confirmIsOpen
    });    
    event.preventDefault();
  }

  toggleSuccessModal = () => {
    this.setState({
      confirmIsOpen: false
    });
    this.setState({
      successIsOpen: !this.state.successIsOpen
    });
  }
  
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
  
  render() {
    return [
      <div className="general-component-bg" key="registerForm">
        <div className="container">
          <div className="card">
            <div className="card-header">
              <h1>Create an Account</h1>
            </div>
            <div className="card-body">
              <form onSubmit={this.handleSubmit}>
                <div className="form-group">
                  To create an account, fill in the required fields, then click "Next."
                </div>
                <div className="form-group">
                  <input required type="text" className="form-control" id="fullname" name="fullname" placeholder="Full Name" onChange={this.handleChange}/>
                </div>
                <div className="form-group">
                  <input required type="text" className="form-control" id="username" name="username" placeholder="Username" onChange={this.handleChange}/>
                </div>
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
                
                <Button type="submit" variant="primary" className="float-right">Next</Button>
                <div className="float-left">
                  Already have a Chariot account? <Link to="/"> Log In</Link>
                </div>
                <br></br>
                <br></br>
              </form>
            </div>
          </div>
        </div>
      </div>,

      <Modal show={this.state.confirmIsOpen} key="registerConfirmModal">
        <Modal.Body>
          Is this information for your account correct?
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

      <Modal show={this.state.successIsOpen} key="registerSuccessModal">
        <Modal.Body>Please check your email to complete the account creation process.</Modal.Body>
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