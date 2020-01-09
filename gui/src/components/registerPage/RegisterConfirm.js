import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class RegisterConfirm extends Component {
  constructor (props) {
    super(props);
  }

  render() {
    return (
      <div className="general-component-bg">
        <div className="container">
          <div className="card">
            <div className="card-header">
            <h1>Confirm Account Information</h1>
              <p>Please confirm that the information about your account is correct, then click "Confirm" to create the account.</p>
            </div>
            <div className="card-body">
              <p>
                <b>Name:</b> {this.props.params.fullname}
                <br></br>
                <b>Username:</b> {this.props.params.username}
                <br></br>
                <b>Password:</b> {this.props.params.password}
                <br></br>
                <b>Email Address:</b> {this.props.params.emailAddress}
                <br></br>
                <b>Security Question:</b> {this.props.params.securityQuestion}
                <br></br>
                <b>Security Question Answer:</b> {this.props.params.securityQuestionAnswer}
              </p>

              <br></br>
              
              <Link to="/register">
                <Button variant="primary" className="float-left">Back</Button>
              </Link>
              <Link to="/">
                <Button variant="primary" className="float-right">Confirm</Button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

}

  
export default RegisterConfirm; 