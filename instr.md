Create a script in /helpers_root/dev_scripts_helpers/docker_cleanup.py
that cleans up Docker and Apple container data structures using space

- To select the engines use
--docker_engine "docker" --docker "apple"
  and have the script iterate on docker_engine

- The goal is to remove everything that is not in use

- For each operation
  - Print what would be deleted, how much space is taken
  - Print the taken space before and after

# Check the current space

> docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          26        1         25.21GB   13.03GB (51%)
Containers      130       0         0B        0B
Local Volumes   6         0         15.59GB   15.59GB (100%)
Build Cache     91        0         6.317GB   2.541GB

# Containers

## Report all the running containers
docker ps -a --filter "status=running" --filter "status=paused" --filter "status=restarting"

## Remove stopped containers.
docker container prune -f

# Networks

## Remove all custom networks not currently used by any container
docker network prune -f

# Volumes

## Remove all "dangling" volumes (volumes not attached to any existing container)
docker volume rm $(docker volume ls --filter dangling=true -q)

# Images

## Remove cached images

docker builder prune -a -f
> docker system df

## Remove all "dangling" images (untagged, e.g. <none>:<none> leftover build layers)
docker rmi -f $(docker images --filter dangling=true -qa)

## Report all the images

docker images --format "{{.ID}} {{.Repository}}:{{.Tag}} {{.Size}}" | while read id repo size; do
  created=$(docker inspect -f '{{.Created}}' "$id")
  echo -e "$repo\tBuilt: $created\tSize: $size"
done

python:3.12-slim        Built: 2026-08-25T01:24:57.86294501Z    Size: 144MB
tmp.llm_transform.arm64.c03540fd:latest Built: 2026-08-23T19:58:12.114327588Z   Size: 262MB
causify/helpers:local-saggese-1.6.0     Built: 2026-08-16T18:39:01.138913551Z   Size: 3.14GB
tmp.typst.aarch64.21c9f649:latest       Built: 2026-08-15T17:47:37.830955213Z   Size: 131MB
tmp.typst.arm64.21c9f649:latest Built: 2026-08-15T17:47:37.830955213Z   Size: 131MB
tmp.pandoc_texlive.arm64.55cc717f:latest        Built: 2026-08-15T17:26:19.557605386Z   Size: 5.73GB
tmp.pandoc_texlive.aarch64.55cc717f:latest      Built: 2026-08-15T17:26:19.557605386Z   Size: 5.73GB
tmp.llm_transform.aarch64.070f04c2:latest       Built: 2026-08-15T16:49:59.651305965Z   Size: 261MB
tmp.llm_transform.arm64.070f04c2:latest Built: 2026-08-15T16:49:59.651305965Z   Size: 261MB
tmp.svg_inkscape.aarch64.92f1f856:latest        Built: 2026-08-15T16:41:21.959447294Z   Size: 321MB
tmp.svg_inkscape.arm64.92f1f856:latest  Built: 2026-08-15T16:41:21.959447294Z   Size: 321MB

Sort them by size and by creation date

# Check the current space

> docker system df
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          26        1         25.21GB   13.03GB (51%)
Containers      130       0         0B        0B
Local Volumes   6         0         15.59GB   15.59GB (100%)
Build Cache     91        0         6.317GB   2.541GB

Report before and after
