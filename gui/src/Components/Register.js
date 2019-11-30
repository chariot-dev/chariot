import React from "react";
import { Link } from 'react-router-dom';

function Register() {
  return (
    <div class="container">
      <h1>Create an Account</h1>
      <form>
        <div class="form-group">
          <text>To create an account, fill in the required fields, then click "Next."</text>
        </div>
        <div class="form-group">
          <label for="ownerCreate" class="font-weight-bold">Name:</label>
          <input class="form-control" id="ownerCreate" placeholder="Full Name" />
        </div>
        <div class="form-group">
          <label for="usernameCreate" class="font-weight-bold">Username:</label>
          <input class="form-control" id="usernameCreate" placeholder="Username" />
        </div>
        <div class="form-group">
            <label for="passwordCreate" class="font-weight-bold">Password:</label>
            <input type="password" class="form-control" id="passwordCreate" placeholder="Password" />
            <input type="checkbox" id="showPassword1" />
            <label for="togglePassword"> Show Password</label>
        </div>
        <div class="form-group">
            <label for="reenterPasswordCreate" class="font-weight-bold">Reenter Password:</label>
            <input type="password" class="form-control" id="reenterPasswordCreate" placeholder="Reenter Password" />
            <input type="checkbox" id="showPassword2" />
            <label for="togglePassword"> Show Password</label>
        </div>
        <div class="form-group">
            <label for="emailCreate" class="font-weight-bold">Email:</label>
            <input type="email" class="form-control" id="emailCreate" placeholder="Email Address" />
        </div>
        <div class="form-group">
            <label for="securityQuestionSelect" class="font-weight-bold">Security Question:</label>
            <select id="securityQuestionSelect" class="form-control">
              <option disabled>Select a security question</option>
              <option>What was your first pet's name?</option>
              <option>What is your dad's middle name?</option>
              <option>What city were you born in?</option>
              <option>What is your favorite sport's mascot?</option>
            </select>
        </div>
        <div class="form-group">
            <label for="securityQuestionAnswer" class="font-weight-bold">Security Question Answer:</label>
            <input type="securityQuestionAnswer" class="form-control" id="securityQuestionAnswer" placeholder="Security Question Answer" />
        </div>
      </form>

      <br></br>
      <Link to="Register_Confirm">
        <input type="submit" class="btn btn-primary float-right" value="Next"/>
      </Link>
      <br></br>
      <br></br>
    </div>
  );
}


export default Register;
