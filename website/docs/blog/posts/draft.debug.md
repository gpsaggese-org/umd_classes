pytest_log 

Run ... | 2>&1 tmp.pytest_script.txt

it

> i pytest_failed

pytest -s --log

pytest -s --dbg

Apply '.claude/skills/coding.rules.md:47:## Decompose Dense Method Chain in Assignments' where possible in msml610/tutorials/L08_causal_inference/L08_04_07_metalearners.py and then apply to ipynb

rigrule

Run msml610/tutorials/L08_causal_inference/L08_04_07_metalearners.py in the container 3a71c0a7bf16 and make it pass

Everybody should have 2-3 agents going at very single time

# Run test inside container

> more tmp.sh
i docker_cmd --base-image=623860924167.dkr.ecr.eu-north-1.amazonaws.com/cmamp
--skip-pull --cmd 'bash -c ./script.sh'

> more script.sh
sudo bash -c "(source /venv/bin/activate; pip install libcst)"
pytest linters/test/test_amp_dev_scripts.py::Test_linter_py1::test_linter_ipynb1

i ... -d
