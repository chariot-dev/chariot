import React from "react";
import Dropdown from '../shared/dropdown'
import { Link } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';

function Choose_Network() {
  return (
    <div class="container">
      <h1>Choose a Network</h1>
      <text>Select a network to begin data collection process.</text>

      <Dropdown> </Dropdown>

      <Link to="/databaseContainer">
        <button type="button" class="btn btn-primary container">Next</button>
      </Link>
    </div>
  );
}
  
export default Choose_Network; 