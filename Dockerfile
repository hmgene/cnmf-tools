<<<<<<< HEAD
FROM node:18
WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
=======
# Use micromamba base image
FROM mambaorg/micromamba:latest

COPY . /app/ 
COPY env.yml /app/ 
WORKDIR /app

RUN micromamba env create -f /app/env.yml && micromamba clean --all --yes

RUN echo "micromamba activate cnmf-tools" >> ~/.bashrc

EXPOSE 8000

CMD ["micromamba", "run", "-n", "cnmf-tools", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> refs/remotes/origin/main
