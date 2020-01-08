import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import RegisterConfirm from './RegisterConfirm';

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
      isSubmitted: false
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  handleSubmit(event) {
    console.log("Submitted");
    this.setState({ isSubmitted: true });
    event.preventDefault();
  }
  
  
  render() {
    console.log(this.state.isSubmitted);
    if (this.state.isSubmitted) {
      return (
        <RegisterConfirm params={this.state}></RegisterConfirm>
      );
    }

    return (
      <div className="container">
        <h1>Create an Account</h1>
        <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            To create an account, fill in the required fields, then click "Next."
          </div>
          <div className="form-group">
            <label className="font-weight-bold">Name:</label>
            <input type="text" className="form-control" id="fullname" name="fullname" placeholder="Full Name" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
            <label className="font-weight-bold">Username:</label>
            <input type="username" className="form-control" id="usernameCreate" name="username" placeholder="Username" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
              <label className="font-weight-bold">Password:</label>
              <input type="password" className="form-control" id="passwordCreate" name="password" placeholder="Password" />
              <input type="checkbox" id="showPassword1" />
              <label> Show Password</label>
          </div>
          <div className="form-group">
              <label className="font-weight-bold">Reenter Password:</label>
              <input type="password" className="form-control" id="reenterPasswordCreate" name="password" placeholder="Reenter Password" onChange={this.handleChange}/>
              <input type="checkbox" id="showPassword2" />
              <label> Show Password</label>
          </div>
          <div className="form-group">
              <label className="font-weight-bold">Email:</label>
              <input type="email" className="form-control" id="emailCreate" name="emailAddress" placeholder="Email Address" onChange={this.handleChange}/>
          </div>
          <div className="form-group">
              <label className="font-weight-bold">Security Question:</label>
              <select id="securityQuestionSelect" className="form-control" name="securityQuestion" onChange={this.handleChange}>
                <option selected disabled hidden>Select a security question</option>
                <option>What was your first pet's name?</option>
                <option>What is your dad's middle name?</option>
                <option>What city were you born in?</option>
                <option>What is your favorite sport's mascot?</option>
              </select>
          </div>
          <div className="form-group">
              <label className="font-weight-bold">Security Question Answer:</label>
              <input type="securityQuestionAnswer" className="form-control" id="securityQuestionAnswer" name="securityQuestionAnswer" placeholder="Security Question Answer" onChange={this.handleChange}/>
          </div>
          <br></br>
          <button type="submit" className="btn btn-primary float-right">Next</button>
          <br></br>
          <br></br>
        </form>
      </div>
    );
  }

}


export default Register;
