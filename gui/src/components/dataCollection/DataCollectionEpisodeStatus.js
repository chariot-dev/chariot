import React, {Component} from 'react';
import { Table, Tooltip } from 'react-bootstrap';
//import {Link} from 'react-router-dom';
import Button from 'react-bootstrap/Button';
import socketIOClient from 'socket.io-client';

//import greenCircleImg from "../images/green_circle.png";
//import yellowCircleImg from "../images/yellow_circle.png";
//import redCircleImg from "../images/red_circle.png";
import { LineChart, Line, XAxis, YAxis, Legend, Label } from 'recharts';

const dataCollectionBaseURL = 'http://localhost:5000/chariot/api/v1.0/data';

class DataCollectionEpisodeStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      chosenNetwork: this.props.location.runProps['Network Name'],
      configId: this.props.location.runProps["configId"],
      socketEndpoint: 'http://localhost:5000',
      fakeData: [
        {timeInSeconds: '1', uv: 4000},
        {timeInSeconds: '2', uv: 3000},
        {timeInSeconds: '3', uv: 2000},
        {timeInSeconds: '4', uv: 2780},
        {timeInSeconds: '5', uv: 1890},
        {timeInSeconds: '6', uv: 2390},
        {timeInSeconds: '7', uv: 3490},
        {timeInSeconds: '8', uv: 3400},
        {timeInSeconds: '9', uv: 1700},
        {timeInSeconds: '10', uv: 1800},
        {timeInSeconds: '11', uv: 2300},
        {timeInSeconds: '12', uv: 2560}
      ],
      timeInSeconds: 1,
      socketData: [],
      response: false
    }
  }
/*
  componentDidMount() {
    const { socketEndpoint } = this.state;
    const socket = socketIOClient(socketEndpoint);

    socket.on("data", data => {
      var tempSocketData = this.state.socketData;
      var dataValue = data[0].freeform.data;
      var curSocketData = {'timeInSeconds': this.state.timeInSeconds, 'dataValue': dataValue};
      tempSocketData.push(curSocketData);

      this.setState({ timeInSeconds: this.state.timeInSeconds + 1});
      this.setState({ socketData: tempSocketData });
    })
  }
*/
  componentDidMount() {
    const { socketEndpoint } = this.state;
    const socket = socketIOClient(socketEndpoint);

    socket.on("data", this.handleSocketData); // Socket event listener
  }


  handleSocketData = (data) => {
    console.log(data);
    this.setState({ response: true });

    var tempSocketData = [... this.state.socketData];
    var dataValue = data[0].freeform.data;
    var curSocketData = {'timeInSeconds': this.state.timeInSeconds, 'dataValue': dataValue};
    tempSocketData.push(curSocketData);

    this.setState({ timeInSeconds: this.state.timeInSeconds + 1});
    this.setState({ socketData: tempSocketData });
  }


  generateVisualizer() {
    return (
      <LineChart width={600} height={300} data={this.state.socketData}>
        <XAxis label={{value: "Time (in seconds)", position: "insideBottomRight", dy: 10}} dataKey="timeInSeconds"/>
        <YAxis label={{value: "Device Data", position: "insideLeft", angle: -90}}/>
        <Tooltip/>
        <Legend/>
        <Line type="monotone" dataKey="dataValue" stroke="#8884d8" activeDot={{r: 8}}/>
    </LineChart>
    );
  }
  
  addDataPoint = () => {


    /*
    var updatedData = [... this.state.data];
    // Instead of getting random numbers, will read from socket to get actual device data
    updatedData.push({timeInSeconds: (this.state.data.length+1).toString(), uv: (Math.floor(Math.random() * 10000) + 1), pv: (Math.floor(Math.random() * 10000) + 1), amt: (Math.floor(Math.random() * 5000) + 1)});
    this.setState({data: updatedData});
    */
  }


  endDataCollection = () => {
    console.log("end the data collection episode");

    fetch(dataCollectionBaseURL + '/stop?configId=' + this.state.configId)
    .then(res => res.json())
    .then(
      // On success
      (result) => {
        console.log(result);
      },
      // On error
      (error) => {
        console.log(error.message);
      }
    )
  }


  render() {
    console.log(this.state.socketData);

    const {response} = this.state;

    return [
      <div className="container">
        <h1>Data Collection Episode</h1>
        <p>Data collection episode for {this.state.chosenNetwork}.</p>

        {this.state.socketData.length > 4 ? this.generateVisualizer() : <p>Waiting for data...</p>}

        <Button variant="danger" className="float-right" onClick={this.endDataCollection}>End Data Collection</Button>

        <Button onClick={this.addDataPoint}variant="primary" className="float-left">Add Data Point</Button>

      </div>
    ]
  }
}

export default DataCollectionEpisodeStatus;