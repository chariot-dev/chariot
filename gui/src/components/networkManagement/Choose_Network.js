import React from "react";
import Dropdown from '../shared/dropdown'
import { Link } from 'react-router-dom';

function Choose_Network() {
  return (
    <div class="container">
      <h1>Choose a Network</h1>
      <text>Select a network to begin data collection process.</text>
      <br></br>
      <br></br>

      <Dropdown> </Dropdown>

      <br></br>
      <br></br>
      <Link to="/welcome">
        <button type="button" class="btn btn-primary float-left" value="Back"/>
      </Link>   
      <Link to="/databaseContainer">
        <button type="button" class="btn btn-primary float-right">Next</button>
      </Link>
    </div>
  );
}
  
export default Choose_Network; 