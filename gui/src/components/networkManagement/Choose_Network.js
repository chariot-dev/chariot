import React from "react";
import Dropdown from '../shared/dropdown'
import { Link } from 'react-router-dom';

function Choose_Network() {
  return (
    <div class="container">
      <h1>Choose a Network</h1>
      <text>Select a network to begin data collection process.</text>

      <Dropdown> </Dropdown>

      <Link to="/databaseContainer">
              <button type="button" class="btn btn-primary btn-lg float-right">Next</button>
      </Link>
    </div>
  );
}
  
export default Choose_Network; 