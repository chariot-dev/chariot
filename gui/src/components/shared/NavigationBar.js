import React from "react";
import { Link } from 'react-router-dom';

function NavigationBar() {
  return (
    <nav class="navbar navbar-expand-lg">
        <ul class="navbar-nav">
          <Link to="/" class="nav-item nav-link">
            <li>Home/Login</li>
          </Link>
          <Link to="/Register" class="nav-item nav-link">
            <li>Register</li>
          </Link>
          <Link to="/Welcome" class="nav-item nav-link">
            <li>Welcome</li>
          </Link>
          <Link to="/Network_Manager" class="nav-item nav-link">
            <li>Network_Manager</li>
          </Link>
          <Link to="/Add_Network" class="nav-item nav-link">
            <li>Add_Network</li>
          </Link>
        </ul>
    </nav>
  );
}

export default NavigationBar; 
