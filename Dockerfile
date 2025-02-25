# Use a base image that supports micromamba or install it
FROM ubuntu:20.04

# Install curl and micromamba
RUN apt-get update && apt-get install -y curl bzip2 && \
    curl -L https://micromamba.snakepit.net/arch/x86_64/latest/micromamba-linux-64.tar.bz2 | tar -xj -C /usr/local/bin

# Set default shell to bash
SHELL ["/bin/bash", "-c"]

# Copy the environment.yml file
COPY environment.yml .

# Install dependencies via micromamba and clean up
RUN micromamba install -y -n base -f environment.yml -v && \
    micromamba clean --all --yes

# Set the default shell to use micromamba
SHELL ["micromamba", "run", "-n", "base", "/bin/bash", "-c"]

# Continue with the rest of your Dockerfile...
COPY . .

# Example command to run the container
CMD ["python", "app.py"]

