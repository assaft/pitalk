#!/bin/bash
cd $PITALK_HOME

# create a virtual env for pitalk
pyenv shell 3.11
pip install -m venv venv
pyenv shell --unset 
source venv/bin/activate
pip install --upgrade pip

# install pitalk
pip install -e .

# create a user
create_user


