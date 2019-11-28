import React from "react";

import 'bootstrap/dist/css/bootstrap.css';

function Register() {
  return (
    <div>
      <h1 class="container">Create an Account</h1>
      <form>
        <div class="form-group container">
          To create an account, fill in the required fields, then click "Next."
        </div>
        <div class="form-group container">
          <label for="usernameCreate">Username:</label>
          <input class="form-control" id="usernameCreate" placeholder="Username" />
        </div>
        <div class="form-group container">
            <label for="passwordCreate">Password:</label>
            <input type="password" class="form-control" id="passwordCreate" placeholder="Password" />
        </div>
        <div class="form-group container">
            <label for="reenterPasswordCreate">Reenter Password:</label>
            <input type="password" class="form-control" id="reenterPasswordCreate" placeholder="Reenter Password" />
        </div>
        <div class="form-group container">
            <label for="emailCreate">Email:</label>
            <input type="email" class="form-control" id="emailCreate" placeholder="Email Address" />
        </div>
        <div class="form-group container">
            <label for="emailCreate">Security Question:</label>
        </div>
      </form>
    </div>
  );
}

export default Register;
