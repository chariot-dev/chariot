import React from "react";
import { Link } from 'react-router-dom';


function Network_Manager() {
  return (
    <div class="container">
      <h1>Add a New Network</h1>
      <text>Please confirm that the information about the network is correct, then click "Create Network".</text>
      <br></br>
      <br></br>

      <text class="font-weight-bold">Name:</text>
      <br></br>
      <text class="font-weight-bold">Description:</text>
      <br></br>
      <br></br>
      <br></br>
      
      <Link to="/add_network">
        <input type="button" class="btn btn-primary float-left" value="Back"/>
      </Link>   
      <Link to="/network_manager">
        <input type="submit" class="btn btn-primary float-right" value="Confirm"/>
      </Link>
      

    </div>
  );
}
  
export default Network_Manager; 