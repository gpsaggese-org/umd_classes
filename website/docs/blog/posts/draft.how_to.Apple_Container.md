---
title: "How to Use Apple Container on macOS"
authors:
    - gpsaggese
date: 2026-06-12
description:
draft: true
categories:
    - Developer Tools
---

TL;DR Apple Container is an open-source container runtime for macOS that uses
lightweight VMs via the Virtualization.framework and Kata Containers to run
containers natively, without Docker Desktop.

<!-- more -->

- Apple's Container tool is an open-source project from Apple that provides a
  native container runtime for macOS
    - The project is available at
      [github.com/apple/container](https://github.com/apple/container/releases)
    - It uses the macOS Virtualization.framework to run lightweight VMs
    - The VMs use Kata Containers as the kernel runtime for container isolation

- This is a modern alternative to Docker Desktop for macOS users who want:
    - Better integration with macOS
    - Lower overhead compared to full VM-based solutions
    - An open-source container runtime maintained by Apple

## Installation

- Install via Homebrew:

```bash
> brew install container
```

- Verify the installation:

```bash
> container --version
container CLI version 1.0.0 (build: release, commit: ee848e3)
```

## Configuration

- Create the configuration directory and file:

```bash
> mkdir ~/.config/container/
> vi ~/.config/container/config.toml
```

- Reference the
  [official documentation](https://apple.github.io/container/documentation/) and
  the
  [start-here tutorial](https://github.com/apple/container/blob/main/docs/tutorials/start-here.md)
  for the full config spec
- The configuration controls resource allocation and system settings:
    - **Build resources**: CPU, memory, and builder image for container builds
    - **Container defaults**: CPU and memory limits for running containers
    - **DNS settings**: Domain configuration for the VM network
    - **Kernel path**: Location of the Kata Containers kernel binary
    - **Machine resources**: VM-level CPU, memory, and home directory mount mode
    - **Registry**: Default container registry domain
    - **vminit**: VM initialization image

### Default System Properties

- After starting the system for the first time, the default configuration looks
  like:

```verbatim
[build]
cpus = 2
image = "ghcr.io/apple/container-builder-shim/builder:0.12.0"
memory = "2048mb"
rosetta = true

[container]
cpus = 8
memory = "4gb"

[dns]
domain = "test"

[kernel]
binaryPath = "opt/kata/share/kata-containers/vmlinux-6.18.15-186"
url = "https://github.com/kata-containers/kata-containers/releases/download/3.28.0/kata-static-3.28.0-arm64.tar.zst"

[machine]
cpus = 4
homeMount = "rw"
memory = "8gb"

[network]

[registry]
domain = "docker.io"

[vminit]
image = "ghcr.io/apple/containerization/vminit:0.33.3"
```

- Key things to note:
    - **Rosetta support** is enabled by default for x86 emulation on Apple
      Silicon
    - The **home directory** is mounted read-write into the VM
    - The kernel uses **Kata Containers** for strong VM-level isolation
    - The **build** section is separate from **container** resources, allowing
      different allocations for building vs. running

## Starting the System

- Start the container system daemon:

```bash
> container system start
Launching container-apiserver...
Testing access to container-apiserver...
Verifying machine API server is running...
```

- On first start, it prompts to install the recommended Kata Containers kernel:

```bash
No default kernel configured.
Install the recommended default kernel from
[https://github.com/kata-containers/kata-containers/releases/download/3.28.0/kata-static-3.28.0-arm64.tar.zst]? [Y/n]: Y
Installing kernel...
```

- After the kernel is installed, start the system again:

```bash
> container system start
Launching container-apiserver...
Testing access to container-apiserver...
Verifying machine API server is running...
```

### Checking System Status

- Verify everything is running correctly:

```bash
> container system status
FIELD              VALUE
status             running
appRoot            /Users/saggese/Library/Application Support/com.apple.container/
installRoot        /usr/local/
logRoot
apiserver.version  container-apiserver version 1.0.0
apiserver.commit   ee848e3ebfd7c73b04dd419683be54fb450b8779
apiserver.build    release
apiserver.appName  container-apiserver
```

- The status shows:
    - The system is **running**
    - The application root is in
      `~/Library/Application Support/com.apple.container/`
    - The container API server is version 1.0.0

## Listing Containers

- List all containers (initially empty):

```bash
> container list --all
ID  IMAGE  OS  ARCH  STATE  IP  CPUS  MEMORY  STARTED
```

## Summary

- Apple Container provides a native, open-source container runtime for macOS
- Key benefits:
    - **Native performance**: Uses Virtualization.framework instead of
      hypervisor-based solutions
    - **Strong isolation**: Kata Containers provide hardware-backed VM isolation
    - **Rosetta support**: Run x86 containers on Apple Silicon seamlessly
    - **Home directory access**: Automatic read-write mount of your home
      directory
- Current limitations:
    - Port forwarding requires manual SSH tunneling or a custom proxy
    - Relatively new project with evolving documentation

- This tool is a promising alternative to Docker Desktop for macOS users who
  want a more lightweight, Apple-native solution for container development
