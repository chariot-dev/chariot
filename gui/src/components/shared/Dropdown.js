/*


*/

import React, { Component } from 'react';

class Dropdown extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
        id: this.props.id,
        availableOptions: this.props.availableOptions, // Component that will use a dropdown passes its options through as props
        selectedOption: '', 
        message : ''
    };
    
    this.handleDropdownChange = this.handleDropdownChange.bind(this);
  }


  handleDropdownChange(event) {
    this.setState({ selectedOption: event.target.value });
  }


  parseAvailableOptions= () => {
    var dropdownOptionsElement = [];
    var availableOptions = this.props.availableOptions;

    for (var i = 0; i < availableOptions.length; i++) {
      dropdownOptionsElement.push(<option key={availableOptions[i]} value={availableOptions[i]}>{availableOptions[i]}</option>);
    }
    
    return dropdownOptionsElement;
  }


  render() {
    return (
      <div>
        <select id="" className="form-control" onChange={this.handleDropdownChange} required>
          {this.parseAvailableOptions()}
        </select>
      </div>
    );
  }
}

export default Dropdown; 