import React, {Component} from 'react';
import { Table, Tooltip } from 'react-bootstrap';
import {Link} from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import socketIOClient from 'socket.io-client';
import { LineChart, Line, XAxis, YAxis, Legend } from 'recharts';
import SuccessModalBody from '../shared/SuccessModalBody';

import BaseURL from "../utility/BaseURL";

const dataCollectionBaseURL = BaseURL + 'data';

class DataCollectionEpisodeStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chosenNetwork: this.props.location.runProps["Network Name"],
      devices: this.props.location.runProps["Devices"],
      configId: this.props.location.runProps["configId"],
      socketEndpoint: "http://192.168.99.100:5000", // may still have to change
      dataValNum: 1, // Count of number of data points
      socketData: [], // Contains the socket data the recharts will use to make the visualizer
      response: false, // Have not recived data from socket yet
      successIsOpen: false,
      showHomeButton: false,
      linesElement: []
    }

    this.toggleSuccessModal = this.toggleSuccessModal.bind(this);
  }


  componentDidMount() {
    const { socketEndpoint } = this.state;
    const socket = socketIOClient(socketEndpoint); // Create the socket
    socket.on("data", this.handleSocketData); // Socket event listener, call handleSocketData() on 'data'

    // Give each device a different color line
    var tempLinesElement = [];
    for (var i = 0; i < this.state.devices.length; i++) {
      var lineColor = "";

      switch(i){ // Get a color for the line
        case 0:
          lineColor = "blue";
          break;
        case 1:
          lineColor = "red";
          break;
        case 2:
          lineColor = "green";
          break;
        case 3:
          lineColor = "purple";
          break;
        case 4:
          lineColor = "orange";
          break;
        case 5:
          lineColor = "yellow";
          break;
        default: // Can't go on forever, so generate random color from here
          var letters = '0123456789ABCDEF';
          var color = '#';
          for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
          }
          lineColor = color;
          break;
      }

      tempLinesElement.push(<Line dataKey={this.state.devices[i]} type="monotone" stroke={lineColor} activeDot={{r: 5}} isAnimationActive={false}/>)
    }

    this.setState({ linesElement: [... tempLinesElement]});
  }


  handleSocketData = (data) => {
    this.setState({ response: true }, function() {// Have now received data from socket, so set to true to display the visualizer
      var curDataInterval = {"dataValNum": this.state.dataValNum};
      var devicesWithNoData = [... this.state.devices]; // Keep track of what device data wasn't received through this get of the socket

      // Save the data from the socket get
      for (var i = 0; i < data.length; i++) {
        var curDeviceName = data[i].device_name;
        var curDeviceData = data[i].freeform.data;

        curDataInterval[curDeviceName] = curDeviceData;

        var index = devicesWithNoData.indexOf(curDeviceName);
        devicesWithNoData.splice(index, 1);
      }

      this.setState({ dataValNum: this.state.dataValNum + 1 }, function() {
        // Fill in the values for the device that didn't have data from this socket get
        for (var j = 0; j < devicesWithNoData.length; j++) {
          var curDeviceWithNoData = devicesWithNoData[j];

          if (!this.state.socketData[this.state.dataValNum - 3]) {
            curDataInterval[curDeviceWithNoData] = 0;
          }
          else {
            curDataInterval[curDeviceWithNoData] = this.state.socketData[this.state.dataValNum - 3][curDeviceWithNoData];
          }
        }

        var tempSocketData = [... this.state.socketData];
        tempSocketData.push(curDataInterval);

        this.setState({ socketData: tempSocketData });
      });
    });
  }


  // Returns the visualizer
  generateVisualizer() {
    return (
      <LineChart width={1000} height={400} data={this.state.socketData}>
        <XAxis dataKey="dataValNum" stroke="black" label={{value: "Data Value Number", position: "insideBottomRight", dy: 10}}/>
        <YAxis stroke="black" label={{value: "Device Data", position: "insideLeft", angle: -90}}/>
        <Tooltip/>
        <Legend/>
        {this.state.linesElement}
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
