import React, { Component } from 'react';

class SuccessModal extends React.Component {
  render() {
    //Render nothing if the "show" prop is false
    if(!this.props.show) {
      return null;
    }

    return (
      <div className="modal-content">
        <span className="close">&times;</span>
        <p>Some text in the Modal..</p>
      </div>
    );
  }
}

export default SuccessModal;