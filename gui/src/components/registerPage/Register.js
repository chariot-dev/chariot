import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import RegisterConfirm from './RegisterConfirm';
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
      passwordImg: hiddenPasswordImg
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.changePasswordVisibility = this.changePasswordVisibility.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  handleSubmit(event) {
    console.log("Submitted");
    this.setState({ isSubmitted: true });
    event.preventDefault();
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
    if (this.state.isSubmitted) {
      return (
        <RegisterConfirm params={this.state}></RegisterConfirm>
      );
    }

    return (
      <div className="general-component-bg">
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
      </div>
    );
  }

}


export default Register;