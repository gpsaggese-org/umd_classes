#!/bin/bash -xe

cc --model=deepseek/deepseek-v4-flash -p '/notebook.create_api_intro https://gymnasium.farama.org/api/vector and save it in tutorials/gymnasium/gymnasium.05.API.Vector.ipynb' --include-partial-messages --print --output-format=stream-json
