import React from "react";
import Login from './Components/Login'
import Welcome from './Components/Welcome';
import Register from './Components/Register';
import NavigationBar from "./Components/NavigationBar";
import Network_Manager from "./Components/Network_Manager";
import Add_Network from "./Components/Add_Network";
import Add_Network_Confirm from "./Components/Add_Network_Confirm";
import Manage_Existing_Networks from "./Components/Manage_Existing_Networks";
import Delete_Network from "./Components/Delete_Network";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';

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
          <Route path="/add_network" component={Add_Network} />
          <Route path="/add_network_confirm" component={Add_Network_Confirm} />
          <Route path="/manage_existing_networks" component={Manage_Existing_Networks} />
          <Route path="/delete_network" component={Delete_Network} />
        </Switch>
      </div>
    </Router>
  );
}



export default App; 
