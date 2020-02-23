/*


*/

import React, { Component } from 'react';

class Dropdown extends Component {
  constructor(props) {
    super(props);
    
    this.state = {
        id: this.props.id,
        defaultOption: this.props.defaultOption,
        availableOptions: this.props.availableOptions,
        selectedOption: '', 
        message : ''
    };
    
    this.showMenu = this.showMenu.bind(this);
    this.handleDropdownChange = this.handleDropdownChange.bind(this);
  }

  
  showMenu(event) {
    this.setState({ showMenu: true }, () => {
      document.addEventListener('click', this.closeMenu);
    });

    event.preventDefault();
  }


  handleDropdownChange(event) {
    this.setState({ selectedOption: event.target.value });
  }


  parseAvailableOptions= () => {
    var dropdownOptionsElement = [];
    var availableOptions = this.props.availableOptions;

    dropdownOptionsElement.push(<option key="chooseNetworkDropdownTitle" selected default disabled>{this.state.defaultOption}</option>)

    for (var i = 0; i < availableOptions.length; i++) {
      dropdownOptionsElement.push(<option key={availableOptions[i]}>{availableOptions[i]}</option>);
    }
    
    return dropdownOptionsElement;
  }


  render() {
    return (
      <div>
        <select id="" className="form-control" onChange={this.handleDropdownChange}>
          {this.parseAvailableOptions()}
        </select>
      </div>
    );
  }
}

export default Dropdown; 