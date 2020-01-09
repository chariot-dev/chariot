import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import Button from 'react-bootstrap/Button';

class AddNetwork extends Component {
  constructor(props) {
    super(props);
    this.state = {
      newNetworkName: "",
      newNetworkDescription: "",
      isSubmitted: false
    }

    this.handleNetworkAdd = this.handleNetworkAdd.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  handleNetworkAdd(event) {
    console.log("Submitted");
    this.setState({ isSubmitted: true });
    event.preventDefault();
  }
  
  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  render() {
    return (
      <div className="container">
        <h1>Add a New Network</h1>
          <p>Please fill in the fields below to create a network. Then, click "Next".</p>
          <br></br>
          
          <form id="createNetworkForm" onSubmit={this.handleNetworkAdd}>
            <div className="form-group">
              <input className="form-control" id="networkNameInput" name="newNetworkName" placeholder="Name"/>
            </div>
            <div className="form-group">
              <textarea className="form-control" id="networkDescriptionInput" rows="5" name="newNetworkDescription" placeholder="Description"></textarea>
            </div>
            <Link to="/networkManager">
              <Button variant="primary" className="float-left">Back</Button>
            </Link>         
            <Link to="/addNetworkConfirm">
              <Button variant="primary" className="float-right">Next</Button>
            </Link>
        </form>
      </div>
    );
  }

}

export default AddNetwork; 