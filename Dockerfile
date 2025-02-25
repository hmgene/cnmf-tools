FROM mambaorg/micromamba:latest
RUN mkdir /home/mambauser/eggnog
WORKDIR /app
COPY --chown=$MAMBA_USER:$MAMBA_USER . . 
ARG MAMBA_DOCKERFILE_ACTIVATE=1
RUN micromamba install -y --file ./env.yml 
RUN micromamba clean --all --yes
