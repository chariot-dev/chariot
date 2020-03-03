import React from 'react';
import Login from './components/loginPage/Login'
import Welcome from './components/welcomePage/Welcome';
import Register from './components/registerPage/Register';
import NetworkManager from "./components/networkManagement/NetworkManager";
import AddNetwork from "./components/networkManagement/AddNetwork";
import ManageExistingNetworks from "./components/networkManagement/ManageExistingNetworks";
import DeleteNetwork from "./components/networkManagement/DeleteNetwork";
import ChooseNetwork from "./components/networkManagement/ChooseNetwork";
import DatabaseConnection from './components/databaseManagement/DatabaseConnection';
import DataAnalysisMain from "./components/dataAnalysis/DataAnalysisMain";
import NetworkConfigsMain from "./components/networkConfigs/NetworkConfigsMain";
import DeviceConfigsMain from "./components/deviceConfigs/DeviceConfigsMain";
import DataOutputConfigsMain from "./components/dataOutputConfigs/DataOutputConfigsMain";
import AddDeviceHome from "./components/deviceManagement/AddDeviceHome";
import DataCollectionEpisodeStatus from "./components/dataCollection/DataCollectionEpisodeStatus";
import ManageNetworkConfiguration from "./components/networkManagement/ManageNetworkConfiguration";
import ManageDevices from "./components/deviceManagement/ManageDevices";
import ManageDeviceConfiguration from "./components/deviceManagement/ManageDeviceConfiguration";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="chariot-bg overflow-case">
        <Switch>
          <Route path="/" exact component={Login} />
          <Route path="/welcome" component={Welcome} />
          <Route path="/register" component={Register} />
          <Route path="/networkManager" component={NetworkManager} />
          <Route path="/addNetwork" component={AddNetwork} />
          <Route path="/manageExistingNetworks" component={ManageExistingNetworks} />
          <Route path="/deleteNetwork" component={DeleteNetwork} />
          <Route path="/chooseNetwork" component={ChooseNetwork} />
          <Route path="/databaseConnection" component={DatabaseConnection} />
          <Route path="/dataAnalysisMain" component={DataAnalysisMain} />
          <Route path="/networkConfigsMain" component={NetworkConfigsMain} />
          <Route path="/deviceConfigsMain" component={DeviceConfigsMain} />
          <Route path="/dataOutputConfigsMain" component={DataOutputConfigsMain} />
          <Route path="/addDeviceHome" component={AddDeviceHome} />
          <Route path="/DataCollectionEpisodeStatus" component={DataCollectionEpisodeStatus} />
          <Route path="/manageExistingNetwork/:networkName" exact component={ManageNetworkConfiguration} />
          <Route path="/manageExistingDevices/devices/:networkName" exact component={ManageDevices} />
          <Route path="/manageExistingDevices/devices/:networkName/:deviceName" exact component={ManageDeviceConfiguration} />
        </Switch>
      </div>
    </Router>
  );
}

export default App; 
