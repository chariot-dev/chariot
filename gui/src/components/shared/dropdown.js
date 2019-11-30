import React, { Component } from 'react';

class Dropdown extends Component {
  constructor() {
    super();
    
    this.state = {
      showMenu: false,
      showMessage: false,
      chosenNetwork: ''
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
    this.setState({showMessage : true});
  }

  render() {
    var message = "You selected " + this.state.chosenNetwork;
    return (
      <div>
        <button onClick={this.showMenu}>
          Select A Network
        </button>
        
        {
          this.state.showMenu
            ? (
              <div>
                <select
                  className="menu"
                  onChange={this.handleDropdownChange}
                >
                  <option value="AirLab Network">AirLab</option>
                  <option value="Dr.Mongan Network">Dr. Mongan</option>
                </select>
                <p>{message}</p>
              </div>
              
            )
            : (
              null
            )
        }

      </div>
    );
  }
}

export default Dropdown; 