#!/bin/bash -e

TOPDIRS=(
    msml610/tutorials/L05_statistical_learning
    msml610/tutorials/L06_bayesian_networks
#    msml610/tutorials/L07_prob_programming
#    msml610/tutorials/L08_causal_inference
#    msml610/tutorials/L09_kalman_filter
#    msml610/tutorials/L09_multi_armed_bandits
#    msml610/tutorials/L10_causal_discovery
#    msml610/tutorials/L12_reinforcement_learning
#    msml610/tutorials/L9x_refreshers
#    tutorials/Asana
#    tutorials/Autogen
#    tutorials/Ax_Multi_Objective_Optimization
#    tutorials/BambooAI
#    tutorials/CausalML_Diabetes_Study
#    tutorials/causalnex
#    tutorials/crewai
#    tutorials/data_science_packages
#    tutorials/dowhy
#    tutorials/FilterPy
#    tutorials/gCastle
#    tutorials/GitHub_Stats
#    tutorials/GluonTS_COVID19_Prediction
#    tutorials/gymnasium
#    tutorials/Jupyter_Extension_Langchain
#    tutorials/LangChain
#    tutorials/LangChain_LangGraph
#    tutorials/LangGraph
#    tutorials/LlamaIndex
#    tutorials/Neo4j
#    tutorials/OpenAI
#    tutorials/pgmpy
#    tutorials/Prophet
#    tutorials/TensorFlow
#    tutorials/TorchRL_MAC
#    tutorials/tsfresh
#    tutorials/tutorial_data_science
#    tutorials/tutorial_forecast_as_service
#    tutorials/tutorial_langchain
#    tutorials/tutorial_langgraph
#    tutorials/tutorial_openai
#    tutorials/tutorial_pydanticAI
#    tutorials/tutorial_pymc
)

# Loop over Set 1: msml610/tutorials
for dir in "${TOPDIRS[@]}"; do
    DST_DIR="$dir"
    #create_links.py --src_dir class_project/project_template --dst_dir $DST_DIR --replace_links --
    \cp -f class_project/project_template/docker_bash.sh class_project/project_template/docker_build.sh class_project/project_template/docker_clean.sh class_project/project_template/docker_cmd.sh class_project/project_template/docker_exec.sh class_project/project_template/docker_jupyter.sh class_project/project_template/docker_name.sh class_project/project_template/docker_push.sh class_project/project_template/run_jupyter.sh class_project/project_template/utils.sh class_project/project_template/version.sh $DST_DIR
done
