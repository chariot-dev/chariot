/*


*/

import React, { Component } from 'react';
import Dropdown from '../shared/Dropdown';
import Button from 'react-bootstrap/Button';
import { Link } from 'react-router-dom';

const getAllNetworksBaseUrl = 'http://localhost:5000/chariot/api/v1.0/networks/all';
const xhr = new XMLHttpRequest();

class ChooseNetwork extends Component {
  constructor(props) {
    super(props);
    this.state = {
      options: ['jioif']

    }
  }

  componentDidMount () {
    xhr.open('GET', getAllNetworksBaseUrl);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Once a response is received
    xhr.onreadystatechange = () => {
      if (xhr.readyState === XMLHttpRequest.DONE) { // Once the request is done
        if (xhr.status === 200) {
          var responseJsonArray = JSON.parse(xhr.response); // Response is a dictionary 

          var networkNames = [];
          for (var i = 0; i < responseJsonArray.length; i++) {
            networkNames.push(responseJsonArray[i]["NetworkName"]);
          }

          this.setState({options: networkNames})
        }
      }
    }
    
    xhr.send();
  }

  render() {
    return (
      <div className="container">
        <h1>Choose a Network</h1>
        <p className="screenInfo">Select a network to begin data collection process.</p>

        <Dropdown id="chooseNetwork" defaultOption="Select a Network" availableOptions={this.state.options}></Dropdown>

        <Link to="/welcome">
          <Button variant="primary" className="float-left footer-button">Back</Button>
        </Link>
        <Link to="/databaseConnection">
          <Button variant="primary" className="float-right footer-button">Next</Button>
        </Link>
      </div>
    );
  }

}

export default ChooseNetwork; 