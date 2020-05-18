import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

import NetworkDeviceCellScreenTemplate from '../shared/NetworkDeviceCellScreenTemplate';

const dbConfigsBaseUrl = 'http://localhost:5000/chariot/api/v1.0/database';

class ManageExistingDatabaseConfigurations extends Component {
  constructor(props) {
    super(props);
    this.state = {
      existingDatabaseConfigurations: []
    }
  } 


  componentDidMount() {
    fetch(dbConfigsBaseUrl + "/all")
    .then(res => res.json())
    .then(
      // On success
      (receivedDBConfigs) => {
        console.log(receivedDBConfigs);
        var dbConfigJson = receivedDBConfigs; // Response is a JSON OBJECT for this one, not JSON ARRAY like the others
        var updatedDatabaseConfigurationsJsonArray = this.state.existingDatabaseConfigurations;

        for (var key in dbConfigJson) {
          updatedDatabaseConfigurationsJsonArray.push(dbConfigJson[key]);
        }

        this.setState({ existingDatabaseConfigurations: updatedDatabaseConfigurationsJsonArray });

      },
      // On error
      (error) => {
        console.log(error.message);
      }
    )
  }


  render() {
    return (
      <div className="container">
        <h1>Manage Existing Database Configurations</h1>
        <p className="screenInfo">
          Select a database to modify its existing configuration settings.
        </p>
        
        {this.state.existingDatabaseConfigurations ? <NetworkDeviceCellScreenTemplate dataJson={this.state.existingDatabaseConfigurations} withLinks={true} type="manageDatabase"></NetworkDeviceCellScreenTemplate> : null}
        
        <Link to="/databaseManager">
          <Button variant="primary" className="float-left footer-button">Back</Button> 
        </Link>
      </div>
    );
  }

}

export default ManageExistingDatabaseConfigurations; 