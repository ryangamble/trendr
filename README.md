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
1. Copy `hooks/pre-commit` to `.git/hooks`
2. When making a commit, make sure your trendr python venv is active and all packages are installed with
   `pip install -r requirements.txt`
3. On commit, black should automatically reformat the trendr subdirectory if needed
Note: This will likely break committing from Github desktop. Either make commits from the command line or don't setup
the pre-commit and instead run `black trendr` from the root of the project to manually reformat the code