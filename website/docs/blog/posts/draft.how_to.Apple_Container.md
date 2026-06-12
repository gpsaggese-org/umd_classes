# Install
brew install container

https://github.com/apple/container/releases

# Documentation

https://apple.github.io/container/documentation/

mkdir ~/.config/container/
vi ~/.config/container/config.toml

https://github.com/apple/container/blob/main/docs/tutorials/start-here.md

> container system start
Launching container-apiserver...
Testing access to container-apiserver...
Verifying machine API server is running...
No default kernel configured.
Install the recommended default kernel from [https://github.com/kata-containers/kata-containers/releases/download/3.28.0/kata-static-3.28.0-arm64.tar.zst]? [Y/n]: Y
Installing kernel...

> container system start
Launching container-apiserver...
Testing access to container-apiserver...
Verifying machine API server is running...


> container system property list

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


> container list --all
ID  IMAGE  OS  ARCH  STATE  IP  CPUS  MEMORY  STARTED

> container --version
container CLI version 1.0.0 (build: release, commit: ee848e3)

> container system status
FIELD              VALUE
status             running
appRoot            /Users/saggese/Library/Application Support/com.apple.container/
installRoot        /usr/local/
logRoot
apiserver.version  container-apiserver version 1.0.0 (build: release, commit: ee848e3)
apiserver.commit   ee848e3ebfd7c73b04dd419683be54fb450b8779
apiserver.build    release
apiserver.appName  container-apiserver


There is an issue with forwarding a port

ssh -L 8888:192.168.64.3:8888 localhost

> python3 -c "
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
"
Forwarding localhost:8888 -> 192.168.64.3:8888
