FROM mambaorg/micromamba

ENV MAMBA_ROOT_PREFIX=/opt/mamba
DEBIAN_FRONTEND=noninteractive
MICROMAMBA_VERSION=0.16.0

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    wget \
    pkg-config \
    libturbojpeg0-dev \
    libopencv-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy environment.yml file
COPY environment.yml .

# Create and activate the environment
RUN micromamba create -n myenv -f environment.yml && \
    micromamba activate myenv
