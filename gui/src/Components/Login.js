import React from "react";
import { Link } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';

function Login() {
  return (
    <div>
      <h1 class="container text-center">Welcome to Chariot</h1>
      <br></br>
      <form>
        <div class="form-group container">
          If you already have an account, please log in.
        </div>
        <div class="form-group container">
          <label for="usernameInput">Username:</label>
          <input class="form-control" id="usernameInput" placeholder="Enter username" />
        </div>
        <div class="form-group container">
          <label for="passwordInput">Password:</label>
          <input type="password" class="form-control" id="passwordInput" placeholder="Enter password" />
        </div>
        <div class="container">
          <Link to="/Welcome">
            <button type="submit" class="btn btn-primary container">Login</button>
          </Link>
        </div>
      </form>
      <br></br>

      <div class="container">
        Dont have an account?
        <Link to="/Register">
          <a id="createAccountLink"> Create one here</a>
        </Link>
      </div>
    </div>
  );
}

export default Login; 