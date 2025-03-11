const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
const path = require('path');


process.env.PATH = `/usr/local/bin:${process.env.PATH}`;

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Listen for Docker commands from the renderer process
ipcMain.handle('docker-pull', (event, imageName) => {
  return new Promise((resolve, reject) => {
    exec(`docker pull ${imageName}`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error: ${stderr}`);
      } else {
        resolve(stdout);
      }
    });
  });
});

ipcMain.handle('docker-run', (event, imageName) => {
  return new Promise((resolve, reject) => {
    exec(`docker run -d -p 8501:8501 ${imageName}`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error: ${stderr}`);
      } else {
        resolve(stdout);
      }
    });
  });
});

