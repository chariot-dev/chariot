import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import AddDeviceHome from './AddDeviceHome';
import AddDeviceVars from './AddDeviceVars';

class AddDevice extends Component {
  constructor (props) {
    super(props);
  }

  render() {
    return (
      <div class="container">
        <AddDeviceHome></AddDeviceHome>

      </div>
    );
  }
}

export default AddDevice;