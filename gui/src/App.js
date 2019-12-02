import React from "react";
import Login from './components/loginPage/Login'
import Welcome from './components/welcomePage/Welcome';
import Register from './components/registerPage/Register';
import NavigationBar from "./components/shared/NavigationBar";
import Network_Manager from "./components/networkManagement/Network_Manager";
import Add_Network from "./components/networkManagement/Add_Network";
import Add_Network_Confirm from "./components/networkManagement/Add_Network_Confirm";
import Manage_Existing_Networks from "./components/networkManagement/Manage_Existing_Networks";
import Delete_Network from "./components/networkManagement/Delete_Network";
import Choose_Network from "./components/networkManagement/Choose_Network";
import Database_Connection from './components/databaseConnection/DatabaseContainer'
import Register_Confirm from "./components/registerPage/Register_Confirm";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Login} />
          <Route path="/welcome" component={Welcome} />
          <Route path="/register" component={Register} />
          <Route path="/network_manager" component={Network_Manager} />
          <Route path="/add_network" component={Add_Network} />
          <Route path="/add_network_confirm" component={Add_Network_Confirm} />
          <Route path="/manage_existing_networks" component={Manage_Existing_Networks} />
          <Route path="/delete_network" component={Delete_Network} />
          <Route path="/choose_network" component={Choose_Network} />
          <Route path="/databaseContainer" component={Database_Connection} />
          <Route path="/register_confirm" component={Register_Confirm} />
        </Switch>
      </div>
    </Router>
  );
}



export default App; 
