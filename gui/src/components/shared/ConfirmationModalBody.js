import React, {Component} from 'react';
import Modal from 'react-bootstrap/Modal';

class ConfirmationModalBody extends Component {
  constructor(props) {
    super(props);
    this.state = {
      confirmationQuestion: this.props.confirmationQuestion, // Question to ask user to confirm
      confirmationData: this.props.confirmationData // List of labels/values that the user has to confirm
    }
  }

  formatConfirmationData () {
    var confirmationData = this.state.confirmationData;

    var confirmationDataElement = [];

    Object.keys(confirmationData).forEach(function(key) {
      var value = confirmationData[key];
      
      confirmationDataElement.push(<div key={key}><b>{key}</b>: {value}<br></br></div>);
    });

    return confirmationDataElement;
  }

  render() {
    return (
      <Modal.Body>
        <p>
        {this.state.confirmationQuestion}
        </p>
        <div>
          {this.formatConfirmationData()}
        </div>
      </Modal.Body>
    );
  }

}

export default ConfirmationModalBody;