import React from "react";
import { Link } from 'react-router-dom';


function Register_Confirm() {
  return (
    <div class="container">
      <h1>Confirm Account Information</h1>
        <text>Please confirm that the information about your account is correct, then click "Confirm" to create the account.</text>        
      <br></br>
      <br></br>

      <text class="font-weight-bold">Name:</text>
      <br></br>
      <text class="font-weight-bold">Username:</text>
      <br></br>
      <text class="font-weight-bold">Password:</text>
      <br></br>
      <text class="font-weight-bold">Email Address:</text>
      <br></br>
      <text class="font-weight-bold">Security Question:</text>
      <br></br>
      <text class="font-weight-bold">Security Question Answer:</text>
      <br></br>
      <br></br>
      <br></br>

      <Link to="/">
        <input type="button" class="btn btn-primary float-right" value="Confirm"/>
      </Link>
    </div>
  );
}
  
export default Register_Confirm; 