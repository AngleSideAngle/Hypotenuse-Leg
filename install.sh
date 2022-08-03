python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
deactivate
cp secrets_template.py ./src/secrets.py