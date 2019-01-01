##### Main dependencies: #####
1. Python 3.5
2. Flask 1.0.2

##### Quick Start: #####
1. Git clone : [git@github.com:Stanislav-Rybonka/dbx_rest_api.git]
2. cd into project root folder for e.q. cd /dbx_rest_api
3. Create virtualenv: python3 -m venv .venv
4. Install requirements: pip install -r requirements.txt
5. Copy environment independent settings file:
   cp .env.example .env
6. Fill in .env, all keys are required.
7. Turn on debug mode, type in your terminal: export FLASK_DEBUG=True
8. Run application: flask run.