import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

const dataCollectionBaseURL = 'http://localhost:5000/chariot/api/v1.0/data';


class RunConfirmationComponent extends Component {
  constructor(props) {
    super(props);
    console.log(this.props.location);
    this.state = {
        "Network Name": this.props.location.networkProps["Network Name"],
        "Database ID": this.props.location.networkProps["Database ID"],
        "Database Name": this.props.location.networkProps["Database Name"],
        "Database Type": this.props.location.networkProps["Database Type"],
        configurationSettings: {}
    }

    this.handleChange = this.handleChange.bind(this);
  }

  startDataCollection = () => {

      var data = {
          "dbId" : this.state["Database ID"],
          "networkName" : this.state["Network Name"],
          "configId": this.state.configurationSettings["configId"],
          "runTime": parseInt(this.state.configurationSettings["runTime"])
      };

      console.log(this.state);
      console.log(data);

      const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    };

      // Execute the post request to 'postCreateNetworkBaseUrl' with 'requestOptions' using fetch
      fetch(dataCollectionBaseURL, requestOptions)
          .then(res => res.json())
          .then(
              // If post was successful, then the dataCollector has been created, proceed to visualizer
              (result) => {
                  console.log(result);
                  },
              // If post was unsuccessful, update state and display error modal
              (error) => {
                  console.log(error.message);
              }
          )

  };

  // Update state when text field is updated
  handleChange(event) {
    var updatedConfigurationSettings = this.state.configurationSettings; // Store from current state
    updatedConfigurationSettings[event.target.id] = event.target.value; // Update the json
    
    this.setState({ configurationSettings: updatedConfigurationSettings }); // Update the state
  }


  render() {
    return (
        <div className="container">
            <div>
                <h1> Data Collection Configuration Confirmation </h1>
                <p> You have selected the following configuration for the data collection episode: </p>
            </div>
            <div>
                <p> <b>Network Name:</b> {this.state["Network Name"]}</p>
            </div>
            <div>
                <p> <b>Database ID:</b> {this.state["Database ID"]} </p>
            </div>
            <div>
                <p> <b>Database Name:</b> {this.state["Database Name"]} </p>
            </div>
            <div>
                <p> <b>Database Type:</b> {this.state["Database Type"]} </p>
            </div>

            <form>
                <div className="form-group">
                Run Time: <input type="number" className="form-control" id="runTime" onChange={this.handleChange}/>
                </div>
                <div className="form-group">
                Configuration Name: <input className="form-control" id="configId" onChange={this.handleChange}/>
                </div>

                <Link to="/chooseNetwork">
                    <Button variant="primary" className="float-left footer-button">Back</Button>
                </Link>
                <Link to={{ pathname: "/dataCollectionEpisodeStatus", networkProps:{"Network Name": this.state["Network Name"]} }}>
                    <Button type="submit" variant="primary" className="float-right footer-button" onClick={this.startDataCollection}>Begin Collection</Button>
                </Link>
            </form>

        </div>
    );
  }
  
}

export default RunConfirmationComponent;