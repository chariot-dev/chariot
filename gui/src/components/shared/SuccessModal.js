import React from 'react';
import successImg from "../images/success.png";

class SuccessModal extends React.Component {
  render() {
    //Render nothing if the "show" prop is false
    if(!this.props.show) {
      return null;
    }

    return (
      <div>
          <img id="successModal" src={successImg} alt="Success"></img>
      </div>
    );
  }
}

export default SuccessModal;