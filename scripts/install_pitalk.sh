#!/bin/bash
set -e 

# create a virtual env for pitalk
pyenv local 3.11
python -m venv venv
source venv/bin/activate
pip install --upgrade pip

# install pitalk
pip install -e .

# create a user
create_user
