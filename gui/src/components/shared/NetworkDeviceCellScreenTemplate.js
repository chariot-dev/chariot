/*
  Template used for screens that separate networks/database configurations into individual cells on the screen
*/

import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

import './NetworkDeviceCellScreenTemplate.css';

class NetworkDeviceCellScreenTemplate extends Component {
  constructor(props) {
    super(props);
    this.state = {
      dataJson: this.props.dataJson,
      withLinks: this.props.withLinks, // withLinks = true means clicking on network/devices is possible
      type: this.props.type // manage, delete, choose
    }
  }
  
  // Call callback function from parent component, ChooseDatabaseConfig
  handleTestDatabaseConnection = (curDatabaseId, curDatabaseName, curDatabaseType, curDatabaseHost) => {
    this.props.testDatabaseConnection(curDatabaseId, curDatabaseName, curDatabaseType, curDatabaseHost);
  }

  // Create individual "cells," or sections, on the screen for each individual network/database
  createCells = () => {
    var links = [];

    for (var i = 0; i < this.state.dataJson.length; i++) {
      // For database page use 
      let curDatabaseId;
      let curDatabaseName;
      let curDatabaseType;
      let curDatabaseHost;

      var deviceTags = []; // Reset list of devices for network-to-be-displayed
      var curNetworkName = this.state.dataJson[i]["NetworkName"];
      var curNetworkDevices = this.state.dataJson[i]["Devices"];
      var curNetworkDescription = this.state.dataJson[i]["Description"];
      let curDevices;

      var buttonElement = [];

      switch (this.state.type) {
        // For DeleteNetwork
        case "delete":
          deviceTags = []; // Reset list of devices for network-to-be-displayed
          curNetworkName = this.state.dataJson[i]["NetworkName"];
          curNetworkDescription = this.state.dataJson[i]["Description"];
    
          buttonElement.push(
            <Button key={"deleteNetworkButton" + i} className="float-right" variant="danger" size="sm" onClick={this.props.deleteNetwork.bind(this, curNetworkName)}>
              Delete Network
            </Button>
          )            
          break;
        // For ManageExistingNetworks
        case "manage":
          deviceTags = []; // Reset list of devices for network-to-be-displayed
          curNetworkName = this.state.dataJson[i]["NetworkName"];
          curNetworkDescription = this.state.dataJson[i]["Description"];
    
          buttonElement.push(
            <Link key={"manageNetworkButton" + i} to={{pathname:'/addDeviceHome', networkProps:{'Network Name': curNetworkName}}}> 
              <Button className="float-right" variant="light" size="sm">
                Add Device
              </Button>
            </Link>
          )
          break;
        // For ChooseNetwork
        case "chooseNetwork":
          deviceTags = []; // Reset list of devices for network-to-be-displayed
          curNetworkDevices = this.state.dataJson[i]["Devices"];
          curNetworkName = this.state.dataJson[i]["NetworkName"];
          curNetworkDescription = this.state.dataJson[i]["Description"];
    
          buttonElement.push(
            <Link key={"chooseNetworkButton" + i} to={{pathname:'/chooseDatabaseConfig', networkProps:{'Network Name': curNetworkName, 'Devices': curNetworkDevices}}}> 
              <Button className="float-right" variant="success" size="sm">
                Choose Network
              </Button>
            </Link>
          )
          break;
        // For ChooseDatabaseConfig
        case "chooseDatabase":
          curNetworkName = this.state.dataJson["chosenNetwork"];
          curDevices = this.state.dataJson["chosenNetworkDevices"];
          curDatabaseId = this.state.dataJson[i]["dbId"];
          curDatabaseHost = this.state.dataJson[i]["host"];
          curDatabaseName = this.state.dataJson[i]["databaseName"];
          curDatabaseType =  this.state.dataJson[i]["type"];

          buttonElement.push(         
            <Link 
              key={"chooseDatabaseButton" + i} 
              to={{pathname:'/runConfirmationComponent', networkProps:{'Network Name': curNetworkName, 'Devices': curDevices, 'Database ID': curDatabaseId, 'Database Name': curDatabaseName, 'Database Type': curDatabaseType}}}>
              <Button className="float-right" variant="success" size="sm">
                Choose Database
              </Button>
            </Link>
          )
          buttonElement.push(
            <Button key={"testDatabaseButton" + i}  className="float-right testDatabaseConnectionButton" variant="info" size="sm" onClick={this.handleTestDatabaseConnection.bind(this, curDatabaseId, curDatabaseName, curDatabaseType, curDatabaseHost)} curDatabaseId={curDatabaseId}>
              Test Database Connection
            </Button>
          )     
          break;
        case "deleteDatabase":
          curNetworkName = this.state.dataJson["chosenNetwork"];
          curDatabaseId = this.state.dataJson[i]["dbId"];
          curDatabaseHost = this.state.dataJson[i]["host"];
          curDatabaseName = this.state.dataJson[i]["databaseName"];
          curDatabaseType =  this.state.dataJson[i]["type"];

          buttonElement.push(
            <Button key={"deleteDatabaseConfigurationButton" + i} className="float-right" variant="danger" size="sm" onClick={this.props.deleteDatabaseConfiguration.bind(this, curDatabaseId)}>
              Delete Database Configuration
            </Button>
          )
          break;
          case "manageDatabase":
            curNetworkName = this.state.dataJson["chosenNetwork"];
            curDatabaseId = this.state.dataJson[i]["dbId"];
            curDatabaseHost = this.state.dataJson[i]["host"];
            curDatabaseName = this.state.dataJson[i]["databaseName"];
            curDatabaseType =  this.state.dataJson[i]["type"];
            break;

        default:
          buttonElement.push(undefined);
      }
      
      // Network-related links conditional
      if (this.state.withLinks && this.state.type !== "manageDatabase") {
        var curDeviceKey;
        var curDeviceName;

        // Create links for network's corresponding devices
        if (this.state.dataJson[i]["Devices"].length > 0) {
          for (var k = 0; k < this.state.dataJson[i]["Devices"].length; k++) {
            curDeviceKey = curNetworkName + "Device" + k;
            curDeviceName = this.state.dataJson[i]["Devices"][k];       
            deviceTags.push(
              <div key={curDeviceKey} className="networksDeviceLink">
                <b>Device {k + 1}: </b>
                  <Link to={{pathname:"/manageExistingDevices/devices/" + curNetworkName + "/" + curDeviceName, networkProps:{'Network Name': curNetworkName, 'Device Name': curDeviceName} }}>
                    {curDeviceName}
                  </Link><br></br>
              </div>
            );
          }
        }
        // If now devices, say so
        else {
          deviceTags.push(
            <div key="noDevices" className="networksDeviceLink">
              No devices exist for this network.
            </div>
          );
        }

        // Create links for network, then create the jsx for networks/devices
        links.push(
          <div className="existingNetworkBox" key={i}>
            <div className="existingNetworkCell">

              {buttonElement}
              
              <div>
                <b>Network Name: </b> 
                  <Link to={{pathname:"/manageExistingNetwork/" + curNetworkName, networkProps:{'Network Name': curNetworkName} }}>
                    {curNetworkName}
                  </Link><br></br>
                <b>Description: </b> {curNetworkDescription}<br></br>
              </div>
              {deviceTags}
            </div>
          </div>
        );
      }
      // Database-related links conditional
      else if (this.state.withLinks && this.state.type === "manageDatabase"){
        links.push(
          <div className="existingNetworkBox" key={i}>
            <div className="existingNetworkCell">

              {buttonElement}
              
              <div>
                <b>Database ID: </b> 
                  <Link to={{pathname:"/manageExistingDatabaseConfigurations/" + curDatabaseId, databaseProps:{'Database Id': curDatabaseId} }}>
                    {curDatabaseId}
                  </Link><br></br>



                <b>Database Name: </b> {curDatabaseName}<br></br>
                <b>Database Type: </b> {curDatabaseType}<br></br>
                <b>Database Host: </b> {curDatabaseHost}<br></br>
              </div>
            </div>
          </div>  
        );
      }
      else { // without links in text
        if (this.state.type !== "chooseDatabase" && this.state.type !== "deleteDatabase") {
          if (this.state.dataJson[i]["Devices"].length > 0) {
            for (var j = 0; j < this.state.dataJson[i]["Devices"].length; j++) {
              curDeviceKey = curNetworkName + "Device" + j;
              curDeviceName = this.state.dataJson[i]["Devices"][j];       
              deviceTags.push(
                <div key={curDeviceKey} className="networksDeviceLink">
                  <b>Device {j + 1}: </b>{curDeviceName}<br></br>
                </div>
              );
            }
          }
          // If no devices, say so
          else {
            deviceTags.push(
              <div key={curDeviceKey} className="networksDeviceLink">
                No devices exist for this network.
              </div>
            );
          }
        }

        // Create links for network, then create the jsx for networks/devices
        if (this.state.type !== "chooseDatabase" && this.state.type !== "deleteDatabase") {
          links.push(
            <div className="existingNetworkBox" key={i}>
              <div className="existingNetworkCell">

                {buttonElement}
                
                <div>
                  <b>Network Name: </b> {curNetworkName}<br></br>
                  <b>Description: </b> {curNetworkDescription}<br></br>
                </div>
                {deviceTags}
              </div>
            </div>
          );
        }

        // Links for DB configs
        else {
          links.push(
            <div className="existingNetworkBox" key={i}>
              <div className="existingNetworkCell">

                {buttonElement}
                
                <div>
                  <b>Database ID: </b> {curDatabaseId}<br></br>
                  <b>Database Name: </b> {curDatabaseName}<br></br>
                  <b>Database Type: </b> {curDatabaseType}<br></br>
                  <b>Database Host: </b> {curDatabaseHost}<br></br>
                </div>
              </div>
            </div>          
          );
        }
      }
    }

    return links;
  }


  render() {
    return (
      <div id="networkDeviceCells">
        {this.createCells()}
      </div>
    );
  }
}

export default NetworkDeviceCellScreenTemplate; 