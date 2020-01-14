import React from 'react';
import Login from './components/loginPage/Login'
import Welcome from './components/welcomePage/Welcome';
import Register from './components/registerPage/Register';
import NetworkManager from "./components/networkManagement/NetworkManager";
import AddNetwork from "./components/networkManagement/AddNetwork";
import ManageExistingNetworks from "./components/networkManagement/ManageExistingNetworks";
import DeleteNetwork from "./components/networkManagement/DeleteNetwork";
import ChooseNetwork from "./components/networkManagement/ChooseNetwork";
import DatabaseConnection from './components/databaseConnection/DatabaseContainer';
import DataAnalysisMain from "./components/dataAnalysis/DataAnalysisMain";
import NetworkConfigsMain from "./components/networkConfigs/NetworkConfigsMain";
import DeviceConfigsMain from "./components/deviceConfigs/DeviceConfigsMain";
import DataOutputConfigsMain from "./components/dataOutputConfigs/DataOutputConfigsMain";
import AddDeviceHome from "./components/deviceManagement/AddDeviceHome";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="chariot-bg">
        <Switch>
          <Route path="/" exact component={Login} />
          <Route path="/welcome" component={Welcome} />
          <Route path="/register" component={Register} />
          <Route path="/networkManager" component={NetworkManager} />
          <Route path="/addNetwork" component={AddNetwork} />
          <Route path="/manageExistingNetworks" component={ManageExistingNetworks} />
          <Route path="/deleteNetwork" component={DeleteNetwork} />
          <Route path="/chooseNetwork" component={ChooseNetwork} />
          <Route path="/databaseContainer" component={DatabaseConnection} />
          <Route path="/dataAnalysisMain" component={DataAnalysisMain} />
          <Route path="/networkConfigsMain" component={NetworkConfigsMain} />
          <Route path="/deviceConfigsMain" component={DeviceConfigsMain} />
          <Route path="/dataOutputConfigsMain" component={DataOutputConfigsMain} />
          <Route path="/addDeviceHome" component={AddDeviceHome} />
        </Switch>
      </div>
    </Router>
  );
}



export default App; 
