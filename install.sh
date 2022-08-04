#!/bin/bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
deactivate
cp secret_template.py ./src/secret.py