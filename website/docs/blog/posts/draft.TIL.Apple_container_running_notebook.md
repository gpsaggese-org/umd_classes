---
title: TIL: A workaround to run Jupyter Notebook in Apple Containers
authors:
    - gpsaggese
date: 2026-06-12
description:
draft: true
categories:
    - Developer Tools
---

TL;DR: I've started using Apple Containers and had to work around a limitation
of 

# The Problem

// TODO(ai_gp): Use the link to the GitHub repo dir instead of class_project/project_template/

- I started using Apple containers instead of my standard Docker set up in
  `class_project/project_template/`
- The porting was quite simple: literally just switch `docker` with `container`
- There were some small incompatibilities, e.g..
  - missing `--filter` option in `ls`
  - a different behavior of `--entrypoint ""`
  - issue with reaching a port in a service (e.g., when using Jupyter notebook)

# Port Forwarding

- One current limitation is that port forwarding is not directly built into the
  CLI
    - The VM gets an internal IP address (e.g., `192.168.64.3`)
    - Services running inside the VM on specific ports need explicit forwarding

- The simplest approach is using an SSH tunnel:
  ```bash
  > ssh -L 8888:192.168.64.3:8888 localhost
  ```

- Find the VM's IP address through the system status or by inspecting the VM
  network

- Alternatively, you can use a Python port-forwarding script for more control:

```python
import socket, threading

def forward(src, dst_host, dst_port):
    dst = socket.socket()
    dst.connect((dst_host, dst_port))
    def pipe(a, b):
        try:
            while True:
                d = a.recv(4096)
                if not d: break
                b.sendall(d)
        except: pass
        finally: a.close(); b.close()
    threading.Thread(target=pipe, args=(src, dst), daemon=True).start()
    threading.Thread(target=pipe, args=(dst, src), daemon=True).start()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 8888))
s.listen(10)
print('Forwarding localhost:8888 -> 192.168.64.3:8888')
while True:
    conn, _ = s.accept()
    forward(conn, '192.168.64.3', 8888)
```

- This script creates a simple TCP proxy:
    - It listens on `localhost:8888`
    - Forwards all traffic to `192.168.64.3:8888` inside the VM
    - Uses threading to handle bidirectional data flow
    - This is useful for accessing Jupyter notebooks, web servers, or other
      services running in containers
