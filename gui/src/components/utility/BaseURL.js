const electron = window.require('electron');
const remote = electron.remote;
var BaseURL = 'http://' + remote.process.env.CORE_IP + ':5000/chariot/api/v1.0/';
export default BaseURL;
