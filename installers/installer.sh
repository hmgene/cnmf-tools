#!/bin/bash
echo "Downloading and running Dockerized app..."

# Install Docker if not installed
if ! command -v docker &> /dev/null
then
    echo "Docker not found. Installing..."
    curl -fsSL https://get.docker.com | sh
fi

# Pull and run the Docker container
docker pull myapp-image
docker run -d --name myapp -p 8080:80 myapp-image

echo "App is running at http://localhost:8080"

