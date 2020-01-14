import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import AddDeviceVars from './AddDeviceVars'

// Figure out whether multiple device additions in one-go should be a thing

class AddDeviceHome extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newDeviceNickname: "",
      newDeviceDescription: "",
      newDeviceType: "",
      showDeviceSpecificSettings: false,
      isSubmitted: false,
      confirmIsOpen: false,
      successIsOpen: false
    }

    this.handleDeviceAdd = this.handleDeviceAdd.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleDeviceAdd(event) {
    this.setState({ isSubmitted: true });
    event.preventDefault();
  }
  
  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  toggleDeviceSpecificSettings = () => {
    if (this.state.newDeviceType) {
      this.setState({
        showDeviceSpecificSettings: !this.state.showDeviceSpecificSettings
      });
    }
  }

  render() {
    return (
      <div className="container">
        <h1>Configure New Device Settings</h1>
        <p className="screenInfo">Please fill in the fields for your new device.</p>

        <form id="createDeviceForm" onSubmit={this.handleDeviceAdd}>
            <div className="form-group">
              <input className="form-control" id="newDeviceNickname" name="newDeviceNickname" placeholder="New Device Nickname" onChange={this.handleChange}/>
            </div>
            <div className="form-group">
              <textarea className="form-control" id="newDeviceDescription" rows="3" name="newDeviceDescription" placeholder="New Device Description" onChange={this.handleChange}></textarea>
            </div>
            <div className="form-group">
                <select required className="form-control" id="securityQuestion" name="newDeviceType" onChange={this.handleChange}>
                  <option selected disabled hidden value="">Select a Device Type</option>
                  <option>R420</option>
                  <option>X-Array</option>
                </select>
            </div>

            {/* Device-specific settings show when user chooses a device and clicks Next */}
            <div>
              {this.state.showDeviceSpecificSettings ? <AddDeviceVars params={this.state}></AddDeviceVars> : null}
            </div>

            
            <Link to="/networkManager">
              <Button variant="primary" className="float-left">Back</Button>
            </Link>
            <Button variant="primary" className="float-right" onClick={this.toggleDeviceSpecificSettings}>Next</Button>
        </form>
      </div>
      

    );
  }
}
 
export default AddDeviceHome; 