import React, {Component} from 'react';
import { Table, Tooltip } from 'react-bootstrap';
import {Link} from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import socketIOClient from 'socket.io-client';
import { LineChart, Line, XAxis, YAxis, Legend } from 'recharts';
//import greenCircleImg from "../images/green_circle.png";
//import yellowCircleImg from "../images/yellow_circle.png";
//import redCircleImg from "../images/red_circle.png";
import SuccessModalBody from '../shared/SuccessModalBody';

const dataCollectionBaseURL = 'http://localhost:5000/chariot/api/v1.0/data';

class DataCollectionEpisodeStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chosenNetwork: this.props.location.runProps['Network Name'],
      configId: this.props.location.runProps["configId"],
      socketEndpoint: 'http://localhost:5000',
      dataValNum: 1, // Count of number of data points
      socketData: [], // Contains the socket data the recharts will use to make the visualizer
      response: false, // Have not recived data from socket yet
      successIsOpen: false,
      showHomeButton: false
    }

    this.toggleSuccessModal = this.toggleSuccessModal.bind(this);
  }


  componentDidMount() {
    const { socketEndpoint } = this.state;
    const socket = socketIOClient(socketEndpoint); // Create the socket

    socket.on("data", this.handleSocketData); // Socket event listener, call handleSocketData() on 'data'
  }


  handleSocketData = (data) => {
    this.setState({ response: true }); // Have now received data from socket, so set to true to display the visualizer

    var tempSocketData = [... this.state.socketData]; // ... to spread out the enumerable properties, statement is to save current data
    var dataValue = data[0].freeform.data; // The data value
    var curSocketData = {'dataValNum': this.state.dataValNum, 'Data Value': dataValue};
    tempSocketData.push(curSocketData); // Add new data point to saved data

    // Update state in order to rerender visualizer
    this.setState({ dataValNum: this.state.dataValNum + 1});
    this.setState({ socketData: tempSocketData });
  }


  // Returns the visualizer
  generateVisualizer() {
    return (
      <LineChart width={1000} height={300} data={this.state.socketData}>
        <XAxis dataKey="dataValNum" stroke="black" label={{value: "Data Value Number", position: "insideBottomRight", dy: 10}}/>
        <YAxis stroke="black" label={{value: "Device Data", position: "insideLeft", angle: -90}}/>
        <Tooltip/>
        <Legend/>
        <Line dataKey="Data Value" type="monotone" stroke="#8884d8" activeDot={{r: 6}} isAnimationActive={false}/>
    </LineChart>
    );
  }

  endDataCollection = () => {
    fetch(dataCollectionBaseURL + '/stop?configId=' + this.state.configId)
    .then(res => res.json())
    .then(
      // On success
      (result) => {
        this.setState({ successIsOpen: true })
        this.setState({ showHomeButton: true })
      },
      // On error
      (error) => {
        console.log(error.message);
      }
    )
  }


  toggleSuccessModal(event){
    this.setState({ successIsOpen: !this.state.successIsOpen})
    event.preventDefault();
  }


  render() {
    const {response} = this.state;

    return [
      <div className="container">
        <h1>Data Collection Episode</h1>
        <p>Data collection episode for {this.state.chosenNetwork}.</p>

        {response ? this.generateVisualizer() : <p>Waiting for data...</p>}

        <Button variant="danger" className="float-right" onClick={this.endDataCollection}>End Data Collection</Button>
        {this.state.showHomeButton ? <Link to="/welcome"><Button variant="primary" className="float-left">Go Home</Button></Link>: null}
      </div>,

      <Modal show={this.state.successIsOpen} key="endDataCollectionEpisodeSuccessModal">
        <SuccessModalBody successMessage="The data collection episode has ended.">
        </SuccessModalBody>

        <Modal.Footer>
          <Button variant="primary" className="float-right" onClick={this.toggleSuccessModal}>OK</Button>
        </Modal.Footer>
      </Modal>

    ]
  }
}

export default DataCollectionEpisodeStatus;