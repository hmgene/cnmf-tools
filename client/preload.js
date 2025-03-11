const { contextBridge, ipcRenderer } = require('electron');

// Expose safe APIs for interacting with Docker
contextBridge.exposeInMainWorld('dockerAPI', {
  pullImage: (imageName) => ipcRenderer.invoke('docker-pull', imageName),
  runContainer: (imageName) => ipcRenderer.invoke('docker-run', imageName)
});

