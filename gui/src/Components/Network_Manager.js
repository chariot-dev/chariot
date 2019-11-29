import React from "react";
import { Link } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';

function Network_Manager() {
  return (
    <div class="container">
      <h1>Network Manager</h1>
        <text>Add, delete, or manage a network.</text>
        <br></br>
        <br></br>
        <br></br>
        <Link to="/Add_Network">
           <text>Add a Network</text>
        </Link>
        <br></br>
        <br></br>
        <Link to="/">
          <text>Delete a Network</text>
        </Link>
        <br></br>
        <br></br>
        <Link to="/">
          <text>Manage Existing Networks</text>
        </Link>

    </div>
  );
}
  
export default Network_Manager; 