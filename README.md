![image](https://img.shields.io/badge/calver-YYYY.MM.DD-22bfda.svg "CalVer")
![image](https://travis-ci.org/devsetgo//test-api.svg "Build Status")
![image](app/coverage.svg "Code Coverage")
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
# Test-API a FASTAPI Example

A test/psuedo API to use as sample data or test data. Inspired by [FakeResponse.com](http://www.fakeresponse.com/). Documentation can be found at [devsetgo.com/projects/test-api](https://devsetgo.com/projects/test-api).


### Note
- This requires a *Nix environment to run. (Linux, Unix, Windows 10 WSL (unbuntu tested) and I think Mac OS (I don't use a Mac)
- This should be just consider a **beta version** api at this time.

## Create Environment

- Copy the repo
  ~~~~
  git clone https://github.com/devsetgo/test-api.git
  python3.7 -m venv env
  source env/bin/activate
  cd app
  ~~~~

- Notes:
    - Libraries require Python 3.6 or 3.7
      - Note: I am using [Ubuntu via WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
      - Upgrading (adding) [Python 3.7 to Ubuntu](https://jcutrer.com/linux/upgrade-python37-ubuntu1810) and setting it as the default for Python3
      - Upgrading [Python3 and install venv](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart)
    - You may need to upgrade pip and setuptools first (pip3 install --upgrade pip setuptools)
- Install requirements
  ~~~~
  Production: pip3 install -r requirements.txt
  Development: pip3 install -r requirements/dev.txt
  ~~~~

- Run it

~~~~
UVICORN
    Development:
        uvicorn main:app --port 5000 --reload
        python3 main.py (running Uvicorn from Code - no reload)

    Production:
        uvicorn main:app --workers 2
        python3 main.py (running Uvicorn from code)
        gunicorn -c gunicorn_cfg.py main:app
        # Note: gunicorn is the config for the dockerfile

Docker
    Docker: docker pull mikeryan56/test-api:latest
~~~~

Run Tests
~~~~
python3 -m pytest
~~~~

Create coverage badge
~~~~
    coverage-badge -o coverage.svg -f
~~~~

Pre-Commit & Hooks
    - Follow install instructionsL: [https://pre-commit.com/#install](https://pre-commit.com/#install)
    - pre-commit install
    - pre-commit run -a

## Features
- default
    - [x] GET ***/*** (root) Forward to OpenAPI to ***/docs***
    - [x] GET ***/Information*** endpoint containing basic app info
    - [x] GET ***/joke*** [PyJoke](https://pyjok.es/) list
- todos
    - [x] GET ***/api/v1/todo/list***
    - [x] GET ***/api/v1/todo/list/count***
    - [x] GET ***/api/v1/todo/list/{todoId}***
    - [x] DELETE ***/api/v1/todo/list/{todoId}***
    - [x] PUT ***/api/v1/todo/list/{todoId}***
    - [x] POST ***/api/v1/todo/create/***
- users
    - [x] GET ***/api/v1/users/list***
    - [x] GET ***/api/v1/users/list/count***
    - [x] GET ***/api/v1/users/list/{todoId}***
    - [x] DELETE ***/api/v1/users/list/{todoId}***
    - [x] PUT ***/api/v1/users/list/{todoId}***
    - [x] POST ***/api/v1/users/create/***
    - [x] POST ***/api/v1/users/check-pwd/***
- silly users
    - [x] GET ***/api/v1/silly-users/make-one***
    - [x] GET ***/api/v1/silly-users/list***


## Issues/Bugs

- [ ] None

## TODO

- [x] Refactor by endpoint (sample, user, etc..)
- [x] Create tests
    - [x] Minimum of 80%
    - [ ] Exception Testing
- [ ] Extend API parameters
    - [ ] Pagination
    - [ ] Number of Items per list returned (Max)
    - [ ] Additional Optional for filtering
- [x] Better organization
- [ ] Standardize API pattern for versioning
- Access Controls
  - [ ] Add Access controls and signup
  - [ ] Add JWT/Token access
  - [ ] Rate limiting
- [X] Gunicorn with Uvicorn configuration
- [x] Logging (using [Loguru](https://github.com/Delgan/loguru))
- [X] Setup CI/CD Pipeline for test and deployment
    - [X] [Travis-CI](https://travis-ci.org)
    - [ ] [Azure Pipelines](https://azure.microsoft.com/en-us/services/devops/pipelines/)
        - [ ] Continous Integration
        - [ ] Continous Deployment (Docker Hub Push)
- [ ] Make [Twelve Factor App](https://12factor.net/) ready
    - [x] One codebase tracked in revision control, many deploys
    - [x] Explicitly declare and isolate dependencies
    - [x] Store config in the environment
    - [ ] Treat backing services as attached resources
    - [ ] Strictly separate build and run stages
    - [ ] Execute the app as one or more stateless processes
    - [x] Export services via port binding
    - [x] Scale out via the process model
    - [x] Maximize robustness with fast startup and graceful shutdown
    - [x] Keep development, staging, and production as similar as possible
    - [x] Treat logs as event streams
    - [ ] Run admin/management tasks as one-off processes

- [ ] Build a [cookiecutter](https://github.com/audreyr/cookiecutter) template for future projects similar to the [FastAPI example](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [ ] Add code comments
- Docker
  - [X] Docker Stack example
  - [ ] Docker Swarm example
  - [ ] Kubernetes example
- Tutorials/Documentation
  - [ ] Basic Overview
  - [ ] Explantion of functions
