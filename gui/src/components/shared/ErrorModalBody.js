import React from 'react';
import Modal from 'react-bootstrap/Modal';
import errorImg from "../images/error.png";

class ErrorModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      errorMessage: this.props.errorMessage
    }
  }


  render() {
    return (
      <Modal.Body><span><img src={errorImg} alt="ErrorImage" className="errorConfirmationImg"/>{this.state.errorMessage}</span></Modal.Body>
    );
  }
}

export default ErrorModal;