# SecFePAS Demo

This repository contains a **demo branch** of SecFePAS that provides a fully self-contained Docker environment for running secure inference using pre-built binaries.  

> All necessary binaries, scripts, and pretrained models are included — no need to build OpenCheetah from source.

---

## 1. Repository Contents

The `demo` branch contains the following:

- Dockerfile # Dockerfile to build the runtime image
- build/ # Pre-built binaries and shared libraries
- pretrained/ # Pretrained model weights
- scripts/ # Runtime scripts: run-server.sh, run-client.sh, common.sh
- README.md # This documentation

Clone only the demo branch
```bash
git clone --branch demo --single-branch https://github.com/KanwalBat00l/SecFePAS.git
cd SecFePAS
```
---

## 2. Prerequisites

- Docker installed on your system
- `bash` shell
- At least 10–20 GB free disk space (for Docker image and build files)

> **Note:** You do **not** need to install OpenCheetah or build anything from source — all binaries are included.

---

## 3. Build the Docker Image

From the root of this repository:

```bash
docker build -t secfepas-demo .
```
This builds a Docker image called secfepas-demo.

Includes all binaries, scripts, and pretrained weights.

# 4. Run the Server
docker run --network host -it secfepas-demo bash scripts/run-server.sh cheetah sqnet


cheetah | SCI_HE → backend

sqnet  | resnet50 | sqnet_quantized | resnet50_quantized → model

Logs will be written to the respective server log files in the container.

# 5. Run the Client
docker run --network host -it secfepas-demo bash scripts/run-client.sh cheetah sqnet


Connects to the server running in the previous step.

Performs secure inference using the pre-built binaries.

# 6. Notes

The build/ folder includes all compiled binaries and libraries (e.g., libgemini.so) required to run the demo.

No external dependencies are required beyond Docker.

The scripts/ folder contains helper scripts for running the server and client.

# 7. Troubleshooting

Docker permission issues: If you see permission denied while trying to connect to docker, make sure your user is in the docker group:

sudo usermod -aG docker $USER
newgrp docker


Large files: The pretrained/ folder contains model weights larger than 50 MB, so cloning may take time.
