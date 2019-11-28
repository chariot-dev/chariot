import React from "react";
import { Link } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';

function NavigationBar() {
  return (
    <nav class="navbar navbar-expand-lg">
        <h3>Chariot</h3>

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
        </ul>
    </nav>
  );
}

export default NavigationBar; 
