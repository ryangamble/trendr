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

## Linter Setup
1. From `react-frontend` run `yarn install`
2. Run `yarn global add eslint`
3. Activate your trendr python venv and run `pip install -r requirements.txt`

### Automatic pre-commit script
1. Copy `hooks/pre-commit` to `.git/hooks`

On commit, black and eslint should automatically reformat what it can, or warn you of required changes. If the linters
have issues running on linux/wsl, try this:

2. Modify script to point to bash executable or remove remainder of line on linux/wsl
3. Make script executable `chmod +x pre-commit` for bash


### Manual alternative
The pre-commit script might break committing from Github desktop and may have issues on Windows. If you would like to 
bypass using the pre-commit script, you can run the linters manually from the root of the project with:
1. `black trendr`
2. `eslint react-frontend/src/**/*.js --fix`