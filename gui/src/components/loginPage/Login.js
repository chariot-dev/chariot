import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import hiddenPasswordImg from "../images/hiddenPassword.PNG";
import showPasswordImg from "../images/showPassword.PNG";

import '../../App.css';

class Login extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: "",
      password: "",
      passwordVisible: false,
      passwordImg: hiddenPasswordImg,
      loginSuccess: false
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
    this.setState({ loginSuccess: true });
    event.preventDefault();
    this.props.history.push(`/welcome`);
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
                  <input required className="form-control" id="usernameInput" name="username" placeholder="Username or Email" />
                </div>
                <div className="form-group input-group">
                  <input required type={this.state.passwordVisible ? "text" : "password"} className="form-control" id="passwordInput" name="password" placeholder="Password" />
                  <img id="passwordVisibilityImg" src={this.state.passwordImg} alt="Hide/Show Password" onClick={this.changePasswordVisibility}></img>
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