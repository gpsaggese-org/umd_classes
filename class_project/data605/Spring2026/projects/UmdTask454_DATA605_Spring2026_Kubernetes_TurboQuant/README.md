# Kubernetes TurboQuant

A CLIP image-embedding service deployed on Kubernetes, with TurboQuant
compression on the resulting vectors to shrink the in-memory index ~8x.

The setup imitates a production embedding service: an `embedder` Deployment
serves `POST /embed`, an `ingester` Job reads a dataset and posts batches to
it, and the HPA scales embedder pods up under load.

## Repo layout

- `services/embedder/` — FastAPI + ONNX CLIP. Scaled by the HPA.
- `services/ingester/` — pulls the image tar from Hugging Face, batches the files, POSTs to the embedder.
- `services/compression/` — TurboQuant ADC index used by the demo notebook.
- `k8s/` — manifests (namespace, embedder Deployment/Service/HPA, ingester Job).
- `Dockerfile` — demo container (JupyterLab + analysis deps).
- `setup_cluster.sh` — builds the embedder/ingester images, loads them into
  minikube, applies the static manifests.
- `demo.ipynb` — end-to-end demo (polls for shards, runs TurboQuant, shows recall + visual results).

## Local installs

- [Docker](https://docs.docker.com/engine/install/)
- [minikube](https://minikube.sigs.k8s.io/docs/start/)
- [`kubectl`](https://kubernetes.io/docs/tasks/tools/)
- `bash` — Git Bash works on Windows ([git-scm.com](https://git-scm.com/))

## Running it

From this directory:

```bash
minikube start
minikube addons enable metrics-server
./setup_cluster.sh
```

The first build pulls torch + open_clip into the embedder image and takes a
while; subsequent builds are cached.

In a second terminal, mount the project's `data/` dir into the cluster and
**leave it running**.

```bash
minikube mount "$(pwd)/data:/data"
```

Then build and start the demo container:

```bash
docker build -t tq-demo .
docker run --rm -it -p 8888:8888 -v "$(pwd):/work" tq-demo
```

Open `http://localhost:8888`, then `demo.ipynb`.

In a third terminal, kick off the ingester:

```bash
kubectl apply -f k8s/ingester-job.yaml
```

Four ingester pods download the image tar, POST batches to the embedder
service, and the HPA scales the embedder up under the load. Watch it
happen:

```bash
kubectl get hpa -n turboquant -w
```

When all four shards land in `data/embeddings/`, the notebook continues
through TurboQuant compression, a Recall@10 benchmark, and a grid of the
top results.

## Switching dataset size

By default the ingester pulls a 1,000-image tar from Hugging Face. Larger
options are available — to use them, edit `k8s/ingester-job.yaml` and
change `DATASET_URL` to one of:

- `https://huggingface.co/datasets/twood1/turboquant-art-1k/resolve/main/images_1k.tar` (default)
- `https://huggingface.co/datasets/twood1/turboquant-art-5k/resolve/main/images_5k.tar`
- `https://huggingface.co/datasets/twood1/turboquant-art-50k/resolve/main/images_50k.tar`

## Tearing down

```bash
kubectl delete namespace turboquant
minikube stop
```

## Embedder API

- `POST /embed` — multipart upload, takes `files=[...]`, returns
  `{"embeddings": [[...], ...]}`.
- `GET /healthz` — readiness probe.
- `GET /metrics` — Prometheus metrics.
