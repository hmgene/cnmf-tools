FROM mambaorg/micromamba:2.0.5

WORKDIR /app
COPY . /app
RUN micromamba install --yes --file ./env.yaml && micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1  


