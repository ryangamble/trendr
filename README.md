# Trendr

## Basic Setup
1. Ensure Python 3.9.x is installed on your system (https://www.python.org/downloads/)
2. Ensure docker engine and cli are installed (both come with docker desktop https://docs.docker.com/desktop/)
3. Clone the repo (https://github.com/ryangamble/trendr)
4. Setup and activate a python environment for this project (see https://docs.python.org/3/library/venv.html)

## Running the full application in local docker containers
1. Run `docker-compose up --build -d` from the root of the repo to run the full app 
   (all frontend and backend components) in local docker containers (see https://docs.docker.com/compose/)
2. Access the web frontend at `localhost`
3. Access the flower dashboard at `localhost:5555`

### Running just the backend
For more information on how to run the backend individually, see `trendr/README.md`

### Running just the frontend
For more information on how to run the frontend individually, see `react-frontend/README.md`

## Setup Pre-Commit Linters
1. From the project root, with your trendr python env active, run `pip install -r requirements.txt` to make sure
   that pre-commit is installed
2. From the project root, run `pre-commit install`
3. Attempt to make a commit, linters should run
4. If there is an error, open `.git/hooks/pre-commit` and double-check the she-bang (On Windows you'll likely need to
   change it from `#!/usr/bin/env python` to something like `#!C:\Users\gambl\venvs\trendr\Scripts\python.exe`)

#### Note: 
This will break commits made from Github desktop. You can either commit from the command line, or not setup
the linter and alternatively, from the root of the project, run `black trendr` to manually run black