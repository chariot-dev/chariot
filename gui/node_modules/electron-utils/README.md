# Electron-Utils

[![npm version](https://badge.fury.io/js/electron-utils.svg)](http://badge.fury.io/js/electron-utils) 

Useful utilities for developing Electron apps and modules

## Register App Protocol

Why you need to use file protocol or local file path to locate your files? With the follow code, you can use `app://views/welcome/index.html` to locate `file://path/to/app/views/welcome/index.html`

In `app.js`
```javascript
const utils = require('electron-utils')
utils.registerAppProtocol()
```

## Window Creation and Management

```javascript
const {windows} = require('electron-utils')
const options = {width: 600, height: 400}
windows.createOrActivate('welcome', 'app://views/welcome/index.html', options)
// some time later...
windows.activate('welcome')
```

## IPC Between Browser Window and Main Process

The default ipc methods are too complex. We need just one line

```javascript
// In main process
const {ipc, windows} = require('electron-utils')
ipc.registerIPCHandler('newwin', (url, name) => {
  windows.createOrActivate(name, url, {width: 640, height: 480})
})

// In renderer process (browser window)
const {ipc} = require('electron-utils')
ipc.handleIPCRequest('newwin', ['https://github.com/', 'github'])
```