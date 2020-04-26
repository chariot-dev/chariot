import React, {Component} from 'react';
import {Link} from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';

import ConfirmationModalBody from '../shared/ConfirmationModalBody';
import SuccessModalBody from '../shared/SuccessModalBody';
import ErrorModalBody from '../shared/ErrorModalBody';

const databaseBaseUrl = "http://localhost:5000/chariot/api/v1.0/database"

class DatabaseConnection extends Component {
  constructor(props) {
    super(props);

    this.state = {
      "Network Name": this.props.location["Network Name"],
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
    fetch(databaseBaseUrl + "/supportedDatabases")
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
        console.log(error.message);
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
        fetch(databaseBaseUrl + "/config?dbId=" + this.state['Database Type'])
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
      // don't want the user to fill out the 'Type' on GUI, so removing it from here
      if (curFieldAlias !== 'type') {
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

    }

    return databaseSpecificForm;
  }

  toggleErrorModal = () => {
    this.setState({ errorIsOpen: !this.state.errorIsOpen });
  }

  testConfigurationConnection = () => {
    var formData = this.parseFromTextFields();
    // Post request options
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    };

    fetch(databaseBaseUrl + "/test", requestOptions)
    .then(res => res.json())
    .then(
      // If post was successful, update state and display success modal
      () => {
        this.setState({
          confirmIsOpen: false
        });
        this.setState({
          successIsOpen: !this.state.successIsOpen
        });
      },
      // If post was unsuccessful, update state and display error modal
      (error) => {
        // Once error message is set, then launch the error modal
        this.setState({
          errorMessage: error.message
        }, () => {
          this.setState({ errorIsOpen: !this.state.errorIsOpen });
        });
      }
    )
  };

  //When the create button is clicked, take the values from the text fields and create a database configuration
  createDatabaseConfiguration = () => {
    var formData = this.parseFromTextFields();
    // Post request options
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    };

    fetch(databaseBaseUrl, requestOptions)
    .then(res => res.json())
    .then(
      // If post was successful, update state and display success modal
      () => {
        this.setState({ confirmIsOpen: false });
        this.setState({ successIsOpen: !this.state.successIsOpen });
      },
      // If post was unsuccessful, update state and display error modal
      (error) => {
        // Once error message is set, then launch the error modal
        this.setState({ errorMessage: error.message }, () => {
          this.setState({ errorIsOpen: !this.state.errorIsOpen });
        });
      }
    )
  };

  //Utility method meant to return values from each text field that is filled by user
  parseFromTextFields = () => {
    var dbType = this.state["Database Type"];

    var formData = {};

    for (var i = 0; i < this.state.databaseConfig["MongoDB"].settings.length; i++) {
      //need to match the databaseProperties keys (which align to title in databaseConfig)
      var textFieldTitle = this.state.databaseConfig[dbType].settings[i].title;
      if (textFieldTitle in this.state.databaseProperties) {
        //user has entered a value for this field, add it to payload as the alias
        formData[this.state.databaseConfig[dbType].settings[i].alias] = this.state.databaseProperties[textFieldTitle]
      }
    }

    //database type can't be parsed from text fields, so add that in separately
    formData["type"] = dbType;

    return formData;
  };


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
          <Button variant="primary" className="float-right footer-button" onClick={this.createDatabaseConfiguration}>Create</Button>
        </form>


        <Link to="/chooseNetwork">
            <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>

        <Button variant="success" className="footer-button button-mid-bottom"
                onClick={this.testConfigurationConnection}>Test Connection</Button>

      </div>,

      <Modal show={this.state.successIsOpen} key="addDatabaseConfigSuccessModal">
      <SuccessModalBody successMessage="The database configuration was succesfully added!">
      </SuccessModalBody>

      <Modal.Footer>
        <Link to={{pathname:'/chooseDatabaseConfig', networkProps: {"Network Name": this.state["Network Name"]} }}>
          <Button variant="primary" className="float-right">Continue</Button>
        </Link>
      </Modal.Footer>
    </Modal>,

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