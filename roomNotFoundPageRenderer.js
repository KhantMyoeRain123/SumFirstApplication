const {ipcRenderer}=require('electron')
const returnButton=document.getElementById('return-button')

//route back to home page
returnButton.addEventListener('click',()=>{
    ipcRenderer.send('to-home-page')
})