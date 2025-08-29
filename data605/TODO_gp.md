- Have Docker mount the top git directory
  - Pros
    - all the sym links are visible
    - one can use a container to run code anywhere in the codebase

# TODO:
- Have a way to build all the Docker containers and test them (e.g., docker_bash,
  docker_jupyter)
  - Maybe use unittest or a script
- Have a script to find / replace all the sym links
