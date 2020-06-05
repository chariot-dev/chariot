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
      chosenNetwork: this.props.location.runProps["Network Name"],
      devices: this.props.location.runProps["Devices"],
      configId: this.props.location.runProps["configId"],
      socketEndpoint: "http://localhost:5000",
      dataValNum: 1, // Count of number of data points
      socketData: [], // Contains the socket data the recharts will use to make the visualizer
      response: false, // Have not recived data from socket yet
      successIsOpen: false,
      showHomeButton: false,
      linesElement: [],
      linesElementColorAr: [],
      selectedLine: "all"
    }

    this.toggleSuccessModal = this.toggleSuccessModal.bind(this);
    this.selectLine = this.selectLine.bind(this);
  }


  componentDidMount() {
    const { socketEndpoint } = this.state;
    const socket = socketIOClient(socketEndpoint); // Create the socket
    socket.on("data", this.handleSocketData); // Socket event listener, call handleSocketData() on 'data'

    // Give each device a different color line
    var tempLinesElement = [];
    var tempLinesElementColorAr = [];;

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
      tempLinesElementColorAr.push(lineColor);
      tempLinesElement.push(<Line 
                              dataKey={this.state.selectedLine === 'all' || this.state.selectedLine === this.state.devices[i] ? this.state.devices[i] : 'none'} 
                              type="monotone" 
                              stroke={lineColor} 
                              activeDot={{r: 5}} 
                              isAnimationActive={false}
                            />)
    }

    this.setState({ linesElement: [... tempLinesElement]});
    this.setState({ linesElementColorAr: [... tempLinesElementColorAr]});   
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

  selectLine(event) {
     // If the same line in the legend is selected consecutively, show all lines again, otherwise, show the selected line
     // The trim() makes it so that the name is still displayed correctly in the legend
    let lineSelected = this.state.selectedLine === event.dataKey ? 'all' : event.dataKey.trim();

    this.setState({
      selectedLine: lineSelected,
    },() => {
      var updatedLinesElement = [];
      for (var i = 0; i < this.state.devices.length; i++) {
        updatedLinesElement.push(<Line 
                                dataKey={this.state.selectedLine === 'all' || this.state.selectedLine === this.state.devices[i] ? this.state.devices[i] : this.state.devices[i] + ' '} 
                                type="monotone" 
                                stroke={this.state.linesElementColorAr[i]} 
                                activeDot={{r: 5}} 
                                isAnimationActive={false}
                              />)
      }
  
      this.setState({ linesElement: [... updatedLinesElement]});
    });
  }


  // Returns the visualizer
  generateVisualizer() {
    return (
      <LineChart width={1050} height={450} data={this.state.socketData}>
        <XAxis dataKey="dataValNum" stroke="black" label={{value: "Data Value Number", position: "insideBottomRight", dy: 10}}/>
        <YAxis stroke="black" label={{value: "Device Data", position: "insideLeft", angle: -90}}/>
        <Tooltip/>
        <Legend onClick={this.selectLine}/>
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
        <p>Data collection episode for {this.state.chosenNetwork}. To view device data individually, click on the desired device's name in the legend. To view all, click on that device name again.</p>

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