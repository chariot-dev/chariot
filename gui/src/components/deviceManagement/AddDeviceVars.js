import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class AddDeviceVars extends Component {
  constructor (props) {
    super(props);
  }

  render() {
    return (
      <div>
        <br></br>
        <br></br>
        <p className="screenInfo">Now please fill in the configuration fields for the {this.props.params.newDeviceType} device.</p> 
        <div className="form-group">
          <input className="form-control" id="newDeviceName" name="newDeviceIP" placeholder="Name/IP Address" onChange={this.handleChange}/>
        </div>
        <div className="form-group">
          <input className="form-control" id="newDeviceName" name="newDeviceName" placeholder="Time" onChange={this.handleChange}/>
        </div>
        WILL BE DYNAMIC ACCORDING TO THE DEVICE SELECTED
        <br></br>
        <br></br>
      </div>
    );
  }
}

export default AddDeviceVars;