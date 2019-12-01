import React, { Component } from 'react';

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
            <div>
                <div class="text-center">
                    <h1> Database Connection </h1>
                    <p> Please fill the following fields to connect to a database to store data to</p>
                </div>
                <div class="text-center">
                    <form>
                        <div class="form-group">
                            <label>Host name:</label>
                            <input type="text"
                                name="ipAddress"
                                value={this.state.formControls.ipAddress.value}
                                onChange={this.changeHandler}
                            />
                        </div>

                        <div class="form-group">
                        <label>Username:</label>
                        <input type="text"
                            name="name"
                            value={this.state.formControls.name.value}
                            onChange={this.changeHandler}
                    
                            />
                        </div>

                        <div class="form-group">
                        <label>Password:</label>
                        <input type="password"
                            name="password"
                            value={this.state.formControls.password.value}
                            onChange={this.changeHandler}
                            />
                        </div>
                    </form>
                </div>
                <button type="button" class="btn btn-primary btn-lg">Connect</button>
            </div>
        );
    }

}


export default DatabaseContainer;