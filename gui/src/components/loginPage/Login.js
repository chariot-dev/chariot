import React, { Component } from 'react';
import { Link } from 'react-router-dom';


class Login extends Component {

  render() {
    return (
      <div className="container">
      <h1 class="text-center">Welcome to Chariot</h1>
      <br></br>
      <form>
        <div class="form-group">
          If you already have an account, please log in.
        </div>
        <div class="form-group">
          <label class="font-weight-bold">Username:</label>
          <input class="form-control" id="usernameInput" placeholder="Enter username" />
        </div>
        <div class="form-group">
          <label class="font-weight-bold">Password:</label>
          <input type="password" class="form-control" id="passwordInput" placeholder="Enter password" />
        </div>
        <div>
          <Link to="/Welcome">
            <button type="submit" class="btn btn-primary">Login</button>
          </Link>
        </div>
      </form>
      <br></br>

      <div>
        <text>Dont have an account? </text>
        <Link to="/register">
          <text id="createAccountLink">Create one here</text>
        </Link>
      </div>

    </div>
    );
  }
  
}


export default Login; 