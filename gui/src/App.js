import React from "react";
import Login from './Components/Login'
import Welcome from './Components/Welcome';
import Register from './Components/Register';
import NavigationBar from "./Components/NavigationBar";
import Add_Network from "./Components/Add_Network";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';
import Network_Manager from "./Components/Network_Manager";

function App() {
  return (
    <Router>
      <div className="App">
      <NavigationBar></NavigationBar>
        <Switch>
          <Route path="/" exact component={Login} />
          <Route path="/welcome" component={Welcome} />
          <Route path="/register" component={Register} />
          <Route path="/network_manager" component={Network_Manager} />
          <Route path="/add_network" component= {Add_Network} />
        </Switch>
      </div>
    </Router>
  );
}



export default App; 
