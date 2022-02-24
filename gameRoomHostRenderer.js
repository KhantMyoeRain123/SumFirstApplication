const codeText=document.getElementById('code-text')
const startButton=document.getElementById('start-button')
const startButtonDiv=document.getElementById('start-button-div')
const {ipcRenderer}=require('electron')


ipcRenderer.on('room-code-display',(e,msg)=>{
    codeText.innerText=msg
}
)
startButton.addEventListener('click',()=>{
    startButton.remove(startButton)
    ipcRenderer.send('game-started')
})