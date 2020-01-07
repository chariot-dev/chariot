import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Register from './Register';

class RegisterConfirm extends Component {
  constructor (props) {
    super(props);
  }

  render() {
    return (
      <div className="container">
        <h1>Confirm Account Information</h1>
          <p>Please confirm that the information about your account is correct, then click "Confirm" to create the account.</p>        
        <br></br>
        <br></br>

        <p>
          <b>Name:</b> {this.props.params.fullname}
        <br></br>
        <b>Username:</b> {this.props.params.username}
        <br></br>
        <b>Password:</b> {this.props.params.password}
        <br></br>
        <b>Email Address:</b> {this.props.params.email}
        <br></br>
        <b>Security Question:</b> {this.props.params.securityQuestion}
        <br></br>
        <b>Security Question Answer:</b> {this.props.params.securityQuestionAnswer}
        </p>
        <br></br>
        <br></br>
        <br></br>
        <Link to="/register">
          <button className="btn btn-primary float-left">Back</button>
        </Link>
        <Link to="/">
          <button className="btn btn-primary float-right">Confirm</button>
        </Link>
      </div>
    );
  }

}

  
export default RegisterConfirm; 