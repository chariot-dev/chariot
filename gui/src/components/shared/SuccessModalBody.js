import React from 'react';
import Modal from 'react-bootstrap/Modal';
import successImg from "../images/success.png";

class SuccessModal extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      successMessage: this.props.successMessage
    }
  }


  render() {
    return (
      <Modal.Body><span><img src={successImg} alt="SuccessImage" className="successConfirmationImg"/>{this.state.successMessage}</span></Modal.Body>
    );
  }
}

export default SuccessModal;