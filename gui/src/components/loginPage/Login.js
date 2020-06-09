import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import hiddenPasswordImg from "../images/hiddenPassword.PNG";
import showPasswordImg from "../images/showPassword.PNG";

import '../../App.css';

const loginUrl = 'http://localhost:5000/chariot/api/v1.0/login';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      passwordVisible: false,
      passwordImg: hiddenPasswordImg,
      loginSuccess: false,
      errorMessage: ""
    }

    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.changePasswordVisibility = this.changePasswordVisibility.bind(this);
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  handleSubmit(event) {
    // Verify account credentials for correctness first
    this.login();
    event.preventDefault();
  }

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

    login = () => {
    // Post request's body
    var data = {
      "username": this.state.username,
      "password": this.state.password
    };

    console.log(data);

    // Post request options
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };

    // Execute the post request to 'postCreateNetworkBaseUrl' with 'requestOptions' using fetch
    fetch(loginUrl, requestOptions)
    .then(
      (res) => {
        if (res.status !== 200) {
          return res.json(); // Return the response to the next then()
        }
        else {
          this.setState({ loginSuccess: true }); // Set to true so test connection success modal appears
          this.props.history.push(`/welcome`)
          return; // Since going to then(), return null since no need to parse response
        }
    })
    .then(
      (resJson) => {
        if (resJson) { // If the response exists
          this.setState({ errorMessage: resJson.message }, () => { // Set the error message
            this.setState({ loginSuccess: false }); // Then set test error modal to true
          });
        }
    })
  };

  render() {
    return (
      <div className="general-component-bg">
        <div className="container">
          <div className="text-center">
            <h1 className="chariot-header">Chariot</h1>
            <p className="screenInfo">Collect and analyze data from multiple IoT devices</p>
          </div>
          <div className="card">
            <div className="card-body">
              <form onSubmit={this.handleSubmit}>
                <div className="form-group">
                  To get started, please log in.
                </div>
                <div className="form-group">
                  <input required className="form-control" id="usernameInput" name="username"
                         placeholder="Username"  onChange={this.handleChange}/>
                </div>
                <div className="form-group input-group">
                  <input required type={this.state.passwordVisible ? "text" : "password"} className="form-control"
                         id="passwordInput" name="password" placeholder="Password" onChange={this.handleChange}  />
                  <img id="passwordVisibilityImg" src={this.state.passwordImg} alt="Hide/Show Password"
                       onClick={this.changePasswordVisibility}></img>
                </div>
                <div>
                  <input type="checkbox" id="rememberMe"/> Remember Me
                </div>
                <Button className="login-button" variant="primary" type="submit">
                  Login
                </Button>
              </form>

              <div>
                Dont have an account? <Link to="/register" id="createAccountLink"> Create one here</Link>
              </div>
              <div>
                <Link to="/" id="forgotPasswordLink"> 
                  Forgot password?
                </Link>
              </div>  
            </div>
          </div>
        </div>
      </div>
    );
  }
  
}


export default Login; 