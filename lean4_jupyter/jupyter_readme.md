# Jupyter with Lean4 Kernel - Docker Setup

This Docker container provides a Jupyter environment with Lean4 kernel support.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, but recommended)

## Quick Start

### Using Docker Compose (Recommended)

1. Build and start the container:
   ```bash
   docker compose up -d
   ```

2. Access Jupyter in your browser at:
   ```
   http://localhost:8888
   ```

3. Your notebooks will be saved in the `./notebooks` directory on your host machine.

4. Stop the container:
   ```bash
   docker-compose down
   ```

### Using Docker directly

1. Build the image:
   ```bash
   docker build -t jupyter-lean4 .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8888:8888 -v $(pwd)/notebooks:/workspace --name jupyter-lean4 jupyter-lean4
   ```

3. Access Jupyter in your browser at:
   ```
   http://localhost:8888
   ```

4. Stop the container:
   ```bash
   docker stop jupyter-lean4
   docker rm jupyter-lean4
   ```

## Using Lean4 in Jupyter

1. Create a new notebook
2. Select "Lean 4" as the kernel
3. Start writing Lean code in the cells

Example Lean4 code:
```lean
#eval 2 + 2

def hello : String := "Hello from Lean4!"
#eval hello
```

## Notes

- The Jupyter server runs without authentication by default (suitable for local development)
- Notebooks are persisted in the `./notebooks` directory
- The container uses the stable version of Lean4
- Port 8888 is exposed for Jupyter access

## Troubleshooting

If you encounter issues with the Lean4 kernel:
1. Check that the container is running: `docker ps`
2. View container logs: `docker logs jupyter-lean4`
3. Rebuild the container: `docker-compose up -d --build`

## Customization

You can modify the Dockerfile to:
- Use a specific Lean4 version
- Install additional Python packages
- Add Lean4 dependencies or libraries
