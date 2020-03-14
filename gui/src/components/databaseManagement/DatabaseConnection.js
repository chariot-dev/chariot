import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';

const xhr = new XMLHttpRequest();

const databaseGetBaseUrl = "http://localhost:5000/chariot/api/v1.0/database"

class DatabaseConnection extends Component {
  constructor(props) {
    super(props);

    this.state = {
      chosenNetwork: this.props.location.networkProps['Network Name'], // Network user chose on previous screen
      supportedDatabaseTypes: [],
      'Database Type' : '',
      databaseConfig : {},
      databaseProperties: {},
      showDatabaseSpecificSettings: false,
      errorIsOpen: false
    }

    this.handleChange = this.handleChange.bind(this);
    this.handleDatabaseTypeChange = this.handleDatabaseTypeChange.bind(this);
  }

  // Gets supported database types when page initially loads in order to dynamically fill in select-menu
  componentDidMount() {
    fetch(databaseGetBaseUrl + "/supportedDatabases")
    .then(res => res.json())
    .then(
      (result) => {
        var tempSupportedDatabaseTypes = [];
        for (var key in result) {
          tempSupportedDatabaseTypes.push(key);
        }
        this.setState({supportedDatabaseTypes: tempSupportedDatabaseTypes});
      },
      (error) => {
        console.log(error);
      }
    )
  }

  // Create the option elements for the select-menu
  getSupportedDatabaseTypeOptions = () => {
    var databaseOptionsElement = [];

    for (var k = 0; k < this.state.supportedDatabaseTypes.length; k++) {
      databaseOptionsElement.push(<option>{this.state.supportedDatabaseTypes[k]}</option>);
    }

    return databaseOptionsElement;
  }

  handleChange(event) {
    var updatedDatabaseProperties = this.state.databaseProperties; // Store from current state
    updatedDatabaseProperties[event.target.name] = event.target.value; // Update the json
    
    this.setState({ databaseProperties: updatedDatabaseProperties }); // Update the state
  }

  /*
  As the database type the user selects changes, update that in the state.
  */
  handleDatabaseTypeChange(event) {
    console.log("------- changed --------");
    var lastDatabaseType = this.state['Database Type'];

    if (lastDatabaseType !== event.target.value) { // If database type was changed
      this.setState({'Database Type': event.target.value }, function () { // Update state, then get config for the db type
        fetch(databaseGetBaseUrl + "/config?dbId=" + this.state['Database Type'])
        .then(res => res.json())
        .then(
          (result) => {
            // Update state so can have reference to the config
            this.setState({databaseConfig: result}, function () {
              this.setState({ showDatabaseSpecificSettings: true});
            });
          },
          (error) => {
            console.log(error);
            this.setState({ errorIsOpen: true});
          }
        )
      });

      this.setState({ showDatabaseSpecificSettings: false}); // Reset to false after render to get ready for next render (if use changes database type)
    }
  }

  createDatabaseFields = () => {
    var config = this.state.databaseConfig[this.state['Database Type']].settings;
    var databaseSpecificForm = [];
    console.log(config);
    
    for (var i = 0; i < config.length; i++) {
      var curFieldAlias = config[i].alias;
      var curFieldDescription = config[i].description;
      var curFieldType = config[i].inputType;
      var curFieldTitle = config[i].title;
      var curFieldIsRequired = config[i].required;

      databaseSpecificForm.push(
        <div className="form-group" key={curFieldAlias}>
          {curFieldIsRequired ? <div className="requiredStar">*</div> : ""}
          {curFieldTitle}
          <input type={curFieldType}  required={curFieldIsRequired} className={curFieldType === "checkbox" ? 'deviceCreationFormCheckbox' : 'form-control'} id={curFieldAlias} name={curFieldTitle} onChange={this.handleChange}/>
        </div>
      );
    }

    return databaseSpecificForm;
  }

  toggleErrorModal = () => {
    this.setState({ errorIsOpen: !this.state.errorIsOpen });
  }


  render() {
    console.log(this.state);
    return [
      <div className="container" key="databaseConnectionScreen">
        <h1>Database Connection</h1>
        <p className="screenInfo">Please fill in the following fields to connect to the database that will store the data.</p>

        <div className="form-group">
              <select required className="form-control" id="Database Type Select" name="Database Type" onChange={this.handleDatabaseTypeChange}>
                <option selected disabled hidden value="">Select a Database Type</option>
                {this.getSupportedDatabaseTypeOptions()}
              </select>
          </div>


        <form>
          {this.state.showDatabaseSpecificSettings ? this.createDatabaseFields() : null}
          <Button variant="primary" className="float-right footer-button" type="submit">Connect</Button>
        </form>


        <Link to="/chooseNetwork">
            <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>

        <Button variant="success" className="footer-button button-mid-bottom">Test Connection</Button>

      </div>,

      <Modal show={this.state.errorIsOpen} key="getDatabaseConfigError">

        <ErrorModalBody errorMessage='Could not get database configuration due to an error. Please try again.'>
        </ErrorModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-left" onClick={this.toggleErrorModal}>OK</Button>
        </Modal.Footer>
      </Modal>

    ]
  }




}

export default DatabaseConnection;