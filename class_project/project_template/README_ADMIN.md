# Admin Guide: Docker Template Customization & Maintenance

This guide is to show how to setup Docker-based projects. It explains how to use the template, customize it for your needs, and maintain it over time.

---

## Quick Start for New Projects

### Step 1: Copy the Template

```bash
# Navigate to the template
cd class_project/project_template

# Copy to your new project
cp -r . /path/to/your/new/project
cd /path/to/your/new/project
```

### Step 2: Choose a Base Image

The template includes three Dockerfile options. Choose the one that best fits your project:

| Option | File | Best For |
|--------|------|----------|
| **Standard** | `Dockerfile.ubuntu` | Full Ubuntu environment with system tools |
| **Lightweight** | `Dockerfile.python_slim` | Minimal Python environment; reduced image size |
| **Modern Package Manager** | `Dockerfile.uv` | Fast dependency resolution with [uv](https://docs.astral.sh/uv/) |

**How to choose:**
- **Use Standard** if you need system-level tools (git, curl, graphviz, etc.)
- **Use Python Slim** to minimize image size and build time
- **Use uv** if you want faster, more reliable dependency management

### Step 3: Set Up Your Dockerfile

1. **Keep the reference files**
   ```bash
   # Your Dockerfiles stay as references
   Dockerfile.ubuntu
   Dockerfile.python_slim
   Dockerfile.uv
   ```

2. **Create your working Dockerfile**
   ```bash
   # Copy the one you chose (e.g., Standard)
   cp Dockerfile.ubuntu Dockerfile
   # Now edit Dockerfile with your project-specific changes
   ```

3. **Add your dependencies**
   ```bash
   # For Dockerfile.uv: Create requirements.in with your packages
   echo "numpy\npandas\nscikit-learn" > requirements.in
   
   # Then lock versions to requirements.txt
   pip-compile requirements.in > requirements.txt
   
   # For other Dockerfiles: Add directly to requirements.txt
   ```

### Step 4: Keep Customization Minimal

- **Only modify** what's necessary for your project
- **Use `requirements.txt`** for all Python packages (don't edit Dockerfile for this)
- **Keep `bashrc` and `etc_sudoers`** as-is unless you need custom shell setup
- **Keep base image and Python version** unless you have specific requirements

---

## Understanding the Dockerfile Flow

Each Dockerfile follows the same structure. Here are the key stages:

### Stage 1: Base Image & System Setup

```dockerfile
FROM ubuntu:24.04  # or python:3.12-slim, depending on your requirement
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get -y update && apt-get -y upgrade
```

**Purpose**: Start with a clean base image and disable interactive installation prompts.

**When to customize**: Only change the base image or version if your project has specific requirements (different Ubuntu version, specific Python version, etc.).

---

### Stage 2: System Utilities (Ubuntu-based Dockerfiles only)

```dockerfile
RUN apt install -y --no-install-recommends \
    sudo \
    curl \
    systemctl \
    gnupg \
    git \
    vim
```

**Purpose**: Install essential system tools for development and container management.

**When to customize**: Add **only if needed** for your project:
- `postgresql-client` — for database connections
- `graphviz` — for graph visualizations
- `ffmpeg` — for media processing

**Best practice**: Use `--no-install-recommends` to keep the image small.

---

### Stage 3: Python & Build Tools (Ubuntu-based Dockerfiles only)

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*
```

**Purpose**: Install Python 3, pip, and build tools needed for compiled packages.

**Why venv**: Creates an isolated Python environment separate from system Python.

**When to customize**: Rarely. Only change if you need a specific Python version (e.g., `python3.11` instead of `python3`).

---

### Stage 4: Virtual Environment Setup

```dockerfile
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN python -m pip install --upgrade pip
```

**Purpose**: Create and activate an isolated virtual environment for your project.

**Why this matters**: Ensures reproducibility and prevents dependency conflicts across projects.

**When to customize**: Never. This is a standard best practice.

---

### Stage 5: Jupyter Installation

```dockerfile
RUN pip install jupyterlab
```

**Purpose**: Install Jupyter Lab for interactive development and data exploration.

**When to customize**:
- **Remove** this line if your project doesn't use Jupyter
- **Add extensions** if needed (e.g., `jupyterlab-git`, `jupyterlab-variableinspector`)

---

### Stage 6: Project Dependencies

```dockerfile
COPY requirements.txt /install/requirements.txt
RUN pip install --no-cache-dir -r /install/requirements.txt
```

**Purpose**: Install your project-specific Python packages.

**When to customize**: **This is the primary place to customize.** Define all your dependencies in `requirements.txt`.

**Best practice**:
- **Pin all versions**: `numpy==1.24.0` (not `numpy>=1.20.0`)
- **Use `--no-cache-dir`**: Reduces image size by skipping pip cache
- **For complex dependencies**: Use `requirements.in` with `pip-tools` or `pip-compile`

**Example requirements.txt:**
```
numpy==1.24.0
pandas==2.0.0
scikit-learn==1.2.2
tensorflow==2.13.0
```

---

### Stage 7: Configuration

```dockerfile
COPY etc_sudoers /etc/sudoers
COPY bashrc /root/.bashrc
```

**Purpose**: Apply custom bash configuration and sudo permissions.

**When to customize**:
- **Edit `bashrc`** to add aliases, environment variables, or custom prompt
- **Edit `etc_sudoers`** if additional users need passwordless sudo access

---

### Stage 8: Version Logging
 
```dockerfile
ADD version.sh /install/
RUN /install/version.sh 2>&1 | tee version.log
```
 
**Purpose**: Document the exact versions of Python, pip, Jupyter, and all installed packages.
 
**What it logs**:
- Python 3 version
- pip version
- Jupyter version
- Complete list of all installed Python packages
 
**Why it matters**: Creates a detailed record of your container's environment for troubleshooting and reproducibility.
 
**How to use**: After building, review `version.log` to verify all dependencies installed correctly:
```bash
docker build -t my-project .
cat version.log  # Check all package versions
```
 
**Extending it**: If you need to log additional tools (MongoDB, Node.js, etc.), add them to `version.sh`:
```bash
echo "# mongo"
mongod --version
```

---

### Stage 9: Port Declaration

```dockerfile
EXPOSE 8888
```

**Purpose**: Declare that the container uses port 8888 (informational for Docker).

**When to customize**: Add additional ports if your application needs them (e.g., `EXPOSE 8888 5432 3000`).

---

## Best Practices: Keep It Simple

### The Core Principle

> **Only change what's necessary for your project. Everything else should inherit from the template.**

This approach:
- Makes Dockerfiles easier to understand and maintain
- Keeps images smaller and faster to build
- Simplifies future updates from the template
- Ensures consistency across similar projects

### How to Do It Right

| What | Where | Example |
|------|-------|---------|
| Python packages | `requirements.txt` | `numpy==1.24.0` |
| System tools | Dockerfile `apt-get` section | `postgresql-client` |
| Shell aliases | `bashrc` | `alias jlab="jupyter lab"` |
| Custom scripts | `scripts/` directory | Setup or initialization scripts |
| User permissions | `etc_sudoers` | Grant passwordless sudo |

### Wrong vs. Right Approach

**Wrong**: Embed everything in the Dockerfile
```dockerfile
RUN pip install my-package && python my_setup.py && npm install
```

**Right**: Use separate files and keep Dockerfile clean
```dockerfile
COPY requirements.txt /install/
RUN pip install -r /install/requirements.txt
COPY scripts/setup.sh /install/
RUN /install/setup.sh
```

---

## .dockerignore Policy

### Why It Matters

The `.dockerignore` file prevents unnecessary files from being added to the Docker build context. This:
- **Reduces build time** (fewer files to transfer to Docker daemon)
- **Reduces image size** (only necessary files are included)
- **Improves security** (prevents leaking sensitive data)

### What to Exclude: Category Breakdown

#### 1. Python Artifacts (Always Exclude)
```
__pycache__/
*.pyc
*.pyo
*.pyd
```
**Why**: Compiled bytecode generated at runtime. Regenerated in container, adds bloat.
**Impact**: image size savings.

#### 2. Virtual Environments (Always Exclude)
```
venv/
.venv/
env/
.env/
```
**Why**: Local venvs aren't portable to containers. The Dockerfile creates its own.
**Impact**: Saves 100MB+ per exclusion.

#### 3. Jupyter Checkpoints (Always Exclude)
```
.ipynb_checkpoints/
```
**Why**: Auto-generated by Jupyter, not needed in the image.

#### 4. Git & Version Control (Always Exclude)
```
.git/
.gitignore
.gitattributes
```
**Why**: Repository history not needed at runtime.

#### 5. Docker Build Scripts (Always Exclude)
```
docker_build.sh
docker_push.sh
docker_clean.sh
docker_exec.sh
docker_cmd.sh
docker_bash.sh
docker_jupyter.sh
docker_name.sh
Dockerfile.*
```
**Why**: Local development scripts don't run inside the container.

#### 6. Large Data Files (Recommended)
```
data/
*.csv
*.pkl
*.h5
*.parquet
```
**Why**: Don't ship large training/test data in the image. Mount via volume instead.
**Best practice**:
```bash
docker run -v /path/to/data:/data my-image
```
**Impact**: Can reduce image size by orders of magnitude.

#### 7. Test Files (Project-Dependent)
```
tests/
tutorials/
```
**Why**: Exclude if tests don't run in the container.
**When to include**: If CI/CD runs tests inside the container.

#### 8. Documentation (Recommended)
```
README.md
docs/
*.md
```
**Why**: Not needed at runtime.
**Exception**: Only keep if your app reads these files at runtime.

#### 9. Generated Files (Always Exclude)
```
*.log
*.tmp
*.cache
build/
dist/
```
**Why**: Generated at runtime, not needed in the image.

---

## Workflow: From Template to Your Project

### Complete Setup Checklist

1. **Copy the template**
   ```bash
   cp -r project_template my-new-project
   cd my-new-project
   ```

2. **Keep all reference Dockerfiles**
   ```
   Dockerfile.ubuntu_24_04
   Dockerfile.python_slim
   Dockerfile.uv
   ```

3. **Create your working Dockerfile**
   ```bash
   cp Dockerfile.ubuntu_24_04 Dockerfile
   # Edit Dockerfile with minimal customization
   ```

4. **Add your dependencies**
   ```bash
   # Create/update requirements.txt
   pip freeze > requirements.txt
   # Then manually review and pin versions
   ```

5. **Configure .dockerignore**
   ```bash
   # Review the template .dockerignore
   # Add your project-specific exclusions (e.g., data directories)
   ```

6. **Test the build**
   ```bash
   docker build -t my-project:latest .
   docker run -it my-project:latest bash
   ```

7. **Test Jupyter (if using)**
   ```bash
   ./docker_jupyter.sh -p 8888
   # Visit http://localhost:8888
   ```

8. **Document customizations**
   ```bash
   # In your project README:
   # - Base image chosen and why
   # - Key dependencies
   # - Any Dockerfile modifications
   # - How to build and run
   ```

---

## Maintaining Your Setup

### 1. Version Your Reference Dockerfiles

Keep all three base options in your project for future reference:

```
Dockerfile                  # Your project's working Dockerfile
Dockerfile.ubuntu_24_04     # Standard: Ubuntu with pip
Dockerfile.python_slim      # Lightweight: python:slim with pip
Dockerfile.uv               # Modern: Ubuntu with uv package manager
```

### 2. Document Any Changes

If you modify the Dockerfile, add explanatory comments:

```dockerfile
# Custom: PostgreSQL client for database access
postgresql-client \

# Custom: Node.js for frontend builds
nodejs \
```

### 3. Monitor Package Versions

After each build, review `version.log`:

```bash
docker build -t my-project .
cat version.log  # Check for unexpected version changes
```

### 4. Keep .dockerignore Updated

If you add new directories or files, update `.dockerignore`:

```bash
# Add to .dockerignore if the directory shouldn't be in the image
data/
cache/
.temp/
```

### 5. Contribute Improvements Back

When you improve your project's Docker setup:

1. Test thoroughly in your project
2. Document the improvement clearly
3. Submit back to `project_template`
4. Other projects can adopt it when they update

**Example improvements**:
- Better way to install TensorFlow with GPU support
- Optimized .dockerignore for data science projects
- Security hardening (non-root user setup)

---

## Troubleshooting

### Build is slow
- Check `.dockerignore`: Ensure large directories (data/, .git/) are excluded
- Check Docker daemon: Verify Docker is running properly
- Check layer caching: Docker reuses cached layers; avoid changing early layers

### Image is too large
```bash
# Check layer sizes
docker history my-project:latest

# Remove unnecessary packages or use python_slim base image
```

### Package not found error
- Verify package name in PyPI (packages are case-sensitive)
- Check Python version compatibility
- Pin specific version if needed

### Permission issues in container
- Check `etc_sudoers`: Ensure user has appropriate permissions
- Check file ownership: Ensure COPY doesn't create root-only files

### Jupyter won't connect
```bash
./docker_jupyter.sh -p 8888
# Verify http://localhost:8888 (not https)
# Check firewall if remote access needed
```
