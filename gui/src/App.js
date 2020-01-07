import React, { Component } from 'react';
import Login from './components/loginPage/Login'
import Welcome from './components/welcomePage/Welcome';
import Register from './components/registerPage/Register';
import NavigationBar from "./components/shared/NavigationBar";
import NetworkManager from "./components/networkManagement/NetworkManager";
import AddNetwork from "./components/networkManagement/AddNetwork";
import AddNetworkConfirm from "./components/networkManagement/AddNetworkConfirm";
import ManageExistingNetworks from "./components/networkManagement/ManageExistingNetworks";
import DeleteNetwork from "./components/networkManagement/DeleteNetwork";
import ChooseNetwork from "./components/networkManagement/ChooseNetwork";
import DatabaseConnection from './components/databaseConnection/DatabaseContainer'
import RegisterConfirm from "./components/registerPage/RegisterConfirm";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Login} />
          <Route path="/welcome" component={Welcome} />
          <Route path="/register" component={Register} />
          <Route path="/networkManager" component={NetworkManager} />
          <Route path="/addNetwork" component={AddNetwork} />
          <Route path="/addNetworkConfirm" component={AddNetworkConfirm} />
          <Route path="/manageExistingNetworks" component={ManageExistingNetworks} />
          <Route path="/deleteNetwork" component={DeleteNetwork} />
          <Route path="/chooseNetwork" component={ChooseNetwork} />
          <Route path="/databaseContainer" component={DatabaseConnection} />
          <Route path="/registerConfirm" component={RegisterConfirm} />
        </Switch>
      </div>
    </Router>
  );
}



export default App; 
