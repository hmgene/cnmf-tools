const { app, BrowserWindow } = require("electron");
const { exec } = require("child_process");

app.whenReady().then(() => {
    let win = new BrowserWindow({ width: 800, height: 600 });
    win.loadURL("http://localhost:8080"); // The Dockerized web app

    // Run Docker container when the app starts
    exec("docker run -d --name myapp -p 8080:80 myapp-image", (err, stdout, stderr) => {
        if (err) console.error(`Error: ${stderr}`);
        else console.log(`Docker started: ${stdout}`);
    });
});
