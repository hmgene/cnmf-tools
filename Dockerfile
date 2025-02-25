FROM mambaorg/micromamba:1.5.1
WORKDIR /app
COPY . . 
RUN micromamba install -y -n base -f environment.yml && \
    micromamba clean --all --yes
SHELL ["micromamba", "run", "-n", "base", "/bin/bash", "-c"]
COPY . .
EXPOSE 8000
CMD ["micromamba", "run", "-n", "base", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

