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
        <Link to="/Delete_Network">
          <text>Delete a Network</text>
        </Link>
        <br></br>
        <br></br>
        <Link to="/Manage_Existing_Networks">
          <text>Manage Existing Networks</text>
        </Link>

        <br></br>
        <br></br>

        <Link to="/welcome">
          <input type="button" class="btn btn-primary float-left" value="Back"/>
        </Link>   

    </div>
  );
}
  
export default Network_Manager; 