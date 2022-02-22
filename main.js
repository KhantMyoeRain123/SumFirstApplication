// main.js

// Modules to control application life and create native browser window
const { app, BrowserWindow,ipcMain} = require('electron')
const WebSocket = require('ws');
const crypto=require('crypto')
const ws=new WebSocket("ws://localhost:8001/")
const createWindow = () => {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true,
    },
  })

  // and load the index.html of the app.
  mainWindow.loadFile('homepage.html')


  // Open the DevTools.
  // mainWindow.webContents.openDevTools()
}

const receiveFromServer=()=>{
  ws.addEventListener('message',({data})=>{
    const event=JSON.parse(data)

  })
}
// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  createWindow()

  app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    ws.close(1000)
    app.quit()
  }
})


ipcMain.on('to-game-room-page-join',(e,code)=>{
  
  const event={type:'join-room',code:code,playerName:'James'}
  while (ws.readyState==0)
  {
    //wait if the connection is not yet established
  }
  ws.send(JSON.stringify(event))
  BrowserWindow.getFocusedWindow().loadFile('gameroom.html')
  receiveFromServer()

})



ipcMain.on('to-game-room-page-make',()=>{
  
  randomString=crypto.randomBytes(3).toString('hex')
  const event={type:'make-room',code:randomString,playerName:'James'}
  while (ws.readyState==0)
  {
    //wait if the connection is not yet established
  }
  ws.send(JSON.stringify(event))
  BrowserWindow.getFocusedWindow().loadFile('gameroomhost.html')
  receiveFromServer()

})


// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
