import React from 'react';
import Login from './components/loginPage/Login'
import Welcome from './components/welcomePage/Welcome';
import Register from './components/registerPage/Register';
import NetworkManager from "./components/networkManagement/NetworkManager";
import DatabaseManager from "./components/databaseManagement/DatabaseManager";
import AddNetwork from "./components/networkManagement/AddNetwork";
import ManageExistingNetworks from "./components/networkManagement/ManageExistingNetworks";
import DeleteNetwork from './components/networkManagement/DeleteNetwork';
import DeleteDatabase from "./components/databaseManagement/DeleteDatabase";
import ManageExistingDatabaseConfigurations from './components/databaseManagement/ManageExistingDatabaseConfigurations';
import ManageDatabaseConfiguration from './components/databaseManagement/ManageDatabaseConfiguration';
import ChooseNetwork from "./components/networkManagement/ChooseNetwork";
import DatabaseConnection from './components/databaseManagement/DatabaseConnection';
import ChooseDatabaseConfig from './components/databaseManagement/ChooseDatabaseConfig';
import AddDeviceHome from "./components/deviceManagement/AddDeviceHome";
import DataCollectionEpisodeStatus from "./components/dataCollection/DataCollectionEpisodeStatus";
import ManageNetworkConfiguration from "./components/networkManagement/ManageNetworkConfiguration";
import ManageDevices from "./components/deviceManagement/ManageDevices";
import ManageDeviceConfiguration from "./components/deviceManagement/ManageDeviceConfiguration";
import RunConfirmationComponent from "./components/runConfirmation/RunConfirmationComponent";

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
          <Route path="/chooseDatabaseConfig" component={ChooseDatabaseConfig} />
          <Route path="/addDeviceHome" component={AddDeviceHome} />
          <Route path="/dataCollectionEpisodeStatus" component={DataCollectionEpisodeStatus} />
          <Route path="/manageExistingNetwork/:networkName" exact component={ManageNetworkConfiguration} />
          <Route path="/manageExistingDevices/devices/:networkName" exact component={ManageDevices} />
          <Route path="/manageExistingDevices/devices/:networkName/:deviceName" exact component={ManageDeviceConfiguration} />
          <Route path="/runConfirmationComponent" exact component={RunConfirmationComponent} />
          <Route path="/databaseManager" component={DatabaseManager} />
          <Route path="/deleteDatabaseConfiguration" component={DeleteDatabase} />
          <Route path="/manageExistingDatabaseConfigurations" exact component={ManageExistingDatabaseConfigurations} />
          <Route path="/manageExistingDatabaseConfigurations/:databaseId" exact component={ManageDatabaseConfiguration} />
        </Switch>
      </div>
    </Router>
  );
}

export default App; 
