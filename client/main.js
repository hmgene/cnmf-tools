const { app, BrowserWindow, ipcMain } = require('electron');
const { exec } = require('child_process');
const { shell } = require("electron"); 
const path = require('path');


process.env.PATH = `/usr/local/bin:${process.env.PATH}`;

let win;

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  win.loadFile('index.html');
}


app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

//ipcMain.handle("check-docker", () => {
//  return new Promise((resolve) => {
//    exec("docker --version", (error, stdout, stderr) => {
//      if (error || stderr) {
//        resolve("Docker is not installed.");
//      } else {
//        resolve(`Docker is installed: ${stdout.trim()}`);
//      }
//    });
//  });
//});

ipcMain.handle("check-docker", () => {
  return new Promise((resolve) => {
    exec("docker --version", (error, stdout, stderr) => {
      if (error || stderr) {
        resolve("Docker is not installed.");
      } else {
        // Check if Docker is running
        exec("docker info", (err, out, errStderr) => {
          if (err || errStderr) {
            resolve("Docker is installed but not running.");
          } else {
            resolve(`Docker is installed and running: ${stdout.trim()}`);
          }
        });
      }
    });
  });
});


ipcMain.handle("docker-pull", async (event, imageName) => {
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


ipcMain.handle("docker-run", (event, imageName) => {
  return new Promise((resolve, reject) => {
    // Check if the container is already running
    exec(`docker ps --filter "ancestor=${imageName}" --format "{{.Names}}"`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error: ${stderr}`);
        return;
      }

      const containerName = stdout.trim();

      if (containerName) {
        resolve(`Container "${containerName}" is already running.`);
        shell.openExternal("http://localhost:8501");
      } else {
        exec(`docker run -d -p 8501:8501 ${imageName}`, (error, stdout, stderr) => {
          if (error) {
            reject(`Error: ${stderr}`);
          } else {
            resolve(`Container started successfully: ${stdout}`);
            shell.openExternal("http://localhost:8501");
          }
        });
      }
    });
  });
});



//ipcMain.handle('docker-run', (event, imageName) => {
//  return new Promise((resolve, reject) => {
//    exec(`docker run -d -p 8501:8501 ${imageName}`, (error, stdout, stderr) => {
//      if (error) {
//        reject(`Error: ${stderr}`);
//      } else {
//        resolve(stdout);
//        shell.openExternal("http://localhost:8501");
//      }
//    });
//  });
//});
//
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

