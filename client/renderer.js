document.getElementById('pullButton').addEventListener('click', async () => {
  const imageName = 'ubuntu:latest';  // Replace with the desired image name
  try {
    const result = await window.dockerAPI.pullImage(imageName);
    document.getElementById('output').innerText = `Pulled image: ${result}`;
  } catch (error) {
    document.getElementById('output').innerText = `Error: ${error}`;
  }
});

document.getElementById('runButton').addEventListener('click', async () => {
  const imageName = 'ubuntu:latest';  // Replace with the desired image name
  try {
    const result = await window.dockerAPI.runContainer(imageName);
    document.getElementById('output').innerText = `Container started: ${result}`;
  } catch (error) {
    document.getElementById('output').innerText = `Error: ${error}`;
  }
});

