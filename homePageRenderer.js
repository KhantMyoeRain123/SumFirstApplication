const { ipcRenderer } = require("electron")
const joinButton=document.getElementById('join-button')
const makeGameButton=document.getElementById('make-game-button')
const roomCodeField=document.getElementById('room-code-field')



//route to game pages
joinButton.addEventListener('click',()=>{
    ipcRenderer.send('to-game-room-page-join',roomCodeField.value)
})
makeGameButton.addEventListener('click',()=>{
    ipcRenderer.send('to-game-room-page-make')
})



