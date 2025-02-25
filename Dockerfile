FROM mambaorg/micromamba:latest
RUN mkdir /home/mambauser/eggnog
COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba install -y --file /tmp/env.yaml && micromamba clean --all --yes
