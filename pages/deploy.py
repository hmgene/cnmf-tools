import streamlit as st
import webbrowser
import os
import platform






# Function to guide users to download Docker Desktop
def download_docker():
    if platform.system() == "Windows":
        download_url = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
    elif platform.system() == "Darwin":  # macOS
        download_url = "https://desktop.docker.com/mac/stable/Docker.dmg"
    else:
        download_url = "https://www.docker.com/products/docker-desktop"  # Linux or unsupported OS
    webbrowser.open(download_url)


# Path to your file (local file in the same directory as your Streamlit app)
file_path = "docker_only/cNMF Tools-1.0.0-arm64.dmg"

# Function to handle file download
def download_file():
    with open(file_path, "rb") as file:
        # Create a download button
        st.download_button(
            label="Download cNMF Tools (MAC arm64)",
            data=file,
            file_name="docker_only/cNMF_Tools-1.0.0-arm64.dmg",
            mime="application/x-apple-diskimage"
        )

# Display the download button
download_file()

# Streamlit App Layout
st.title("Tool Downloader & Docker Setup")
st.write(
    """
    Welcome to the tool downloader. Click the button below to download Docker Desktop 
    and run the tool locally. Once Docker Desktop is installed, you can use the tool 
    from your browser on localhost.
    """
)

# Button to trigger Docker download
if st.button("Download Docker Desktop"):
    st.write("Redirecting to Docker download...")
    download_docker()

# Provide instructions for running the tool
st.write(
    """
    After Docker Desktop is installed, you can run the tool locally using the following commands:
    
    1. Open your terminal (Command Prompt or PowerShell on Windows, Terminal on macOS/Linux).
    2. Pull the Docker image:
    
    ```bash
    docker pull <your-docker-image-name>
    ```
    
    3. Run the Docker container:
    
    ```bash
    docker run -d -p 8501:8501 <your-docker-image-name>
    ```

    Now, your tool should be accessible at `http://localhost:8501`.
    """
)


