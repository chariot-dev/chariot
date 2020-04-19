'use strict'

module.exports = {
  registerAppProtocol: require('./lib/protocol'),
  ipc: require('./lib/ipc'),
  windows: require('./lib/windows')
}