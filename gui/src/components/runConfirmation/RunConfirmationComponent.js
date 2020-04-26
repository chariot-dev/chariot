import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class RunConfirmationComponent extends Component {
  constructor(props) {
    super(props);
    console.log(this.props.location);
    this.state = {
        "Network Name": this.props.location.networkProps["Network Name"],
        "Database ID": this.props.location.networkProps["Database ID"],
        "Database Name": this.props.location.networkProps["Database Name"],
        "Database Type": this.props.location.networkProps["Database Type"]
    }
  }

  render() {
    return (
        <div className="container">
            <div>
                <h1> Data Collection Configuration Confirmation </h1>
                <p> You have selected the following configuration for the data collection episode: </p>
            </div>
            <div className="text-center">
                <p> <b>Network Name:</b> {this.state["Network Name"]}</p>
            </div>
            <div className="text-center">
                <p> <b>Database ID:</b> {this.state["Database ID"]} </p>
            </div>
            <div className="text-center">
                <p> <b>Database Name:</b> {this.state["Database Name"]} </p>
            </div>
            <div className="text-center">
                <p> <b>Database Type:</b> {this.state["Database Type"]} </p>
            </div>
            <Link to="/chooseNetwork">
                <Button variant="primary" className="float-left footer-button">Back</Button>
            </Link>
            <Button variant="primary" className="float-right footer-button">Begin Collection</Button>
        </div>
    );
  }
  
}

export default RunConfirmationComponent;