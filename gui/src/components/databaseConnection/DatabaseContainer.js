import React, { Component } from 'react';

import 'bootstrap/dist/css/bootstrap.css';

class DatabaseContainer extends Component {
    constructor(props) {
        super(props);
        this.state = {
            formControls: {
                ipAddress: {
                    value: ''
                },
                name: {
                    value: ''
                },
                password: {
                    value: ''
                }
            }
        }

        this.handleSubmit = this.handleSubmit.bind(this);
    }

    /*
    Currently using the handleSubmit method to try to establish a TCP connection with a database
         if the connection is successful, then show success modal. Otherwise, show failure modal and do
         not proceed to next screen
    */
    handleSubmit(event) {
        //currently assuming that connection will always be established
        this.setState({
            show: true
          });
    }

    changeHandler = event => {

        const name = event.target.name;
        const value = event.target.value;

        this.setState({
            formControls: {
                ...this.state.formControls,
                [name]: {
                    ...this.state.formControls[name],
                    value
                }
            }
        });
    }


    render() {
        return (
            //<form onSubmit={this.handleSubmit}></form>
            <form class="container">

                <label>Host name/address:</label>
                <input type="text"
                    name="ipAddress"
                    value={this.state.formControls.ipAddress.value}
                    onChange={this.changeHandler}
                />

                <label>Username:</label>
                <input type="text"
                    name="name"
                    value={this.state.formControls.name.value}
                    onChange={this.changeHandler}
                    
                />

                <label>Password:</label>
                <input type="password"
                    name="password"
                    value={this.state.formControls.password.value}
                    onChange={this.changeHandler}
                />
            </form>
        );
    }

}


export default DatabaseContainer;