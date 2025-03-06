@echo off
echo Downloading and running Dockerized app...

:: Install Docker if not found
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Docker not found. Please install Docker manually from https://www.docker.com/get-started
    exit /b
)

:: Pull and run Docker container
docker pull myapp-image
docker run -d --name myapp -p 8080:80 myapp-image

echo App is running at http://localhost:8080
pause
