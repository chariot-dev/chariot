import React from "react";
import Login from './Components/Login'
import Welcome from './Components/Welcome';
import Register from './Components/Register';
import NavigationBar from "./Components/NavigationBar";

import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';

import 'bootstrap/dist/css/bootstrap.css';

function App() {
  return (
    <Router>
      <div className="App">
      <NavigationBar></NavigationBar>
        <Switch>
          <Route path="/" exact component={Login}/>
          <Route path="/welcome" component={Welcome}/>
          <Route path="/register" component={Register}/>
        </Switch>
      </div>
    </Router>
  );
}



export default App; 
