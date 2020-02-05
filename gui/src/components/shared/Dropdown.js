/*


*/

import React, { Component } from 'react';

class Dropdown extends Component {
  constructor() {
    super();
    
    this.state = {
        chosenNetwork: '',
        message : ''
    };
    
    this.showMenu = this.showMenu.bind(this);
    this.handleDropdownChange = this.handleDropdownChange.bind(this);
  }

  choseNetwork(networkName) {
    this.chosenNetwork=networkName;
  }
  
  showMenu(event) {
    event.preventDefault();
    
    this.setState({ showMenu: true }, () => {
      document.addEventListener('click', this.closeMenu);
    });
  }

    handleDropdownChange(e) {
        this.setState({ chosenNetwork: e.target.value });
  }

  render() {
    var message = "You selected " + this.state.chosenNetwork;
    return (
      <div>
        <div>
        <p>{message}</p>
        <select className="menu" onChange={this.handleDropdownChange}>
            <option value="AirLab Network">AirLab</option>
            <option value="Dr.Mongan Network">Dr. Mongan</option>
        </select>
        </div>
      </div>
    );
  }
}

export default Dropdown; 