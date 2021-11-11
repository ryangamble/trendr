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
2. When making a commit, make sure your trendr python venv is active and all python/node packages are up to date with
   `pip install -r requirements.txt` and from react-frontend `yarn install`
3. On commit, black and eslint should automatically reformat what it can, or warn you of required changes

### Manual alternative
This might break commiting from Github desktop and may have issues on Windows. If you would like to forgo using
the pre-commit script, you can run the linters manually from the root of the project with:
`black trendr`
`eslint react-frontend/src/**/*.js --fix`