![image](https://img.shields.io/badge/calver-YYYY.MM.DD-22bfda.svg "CalVer")
![image](https://travis-ci.org/devsetgo//test-api.svg "Build Status")
![image](coverage.svg "Code Coverage")
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=alert_status)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=bugs)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)


# Test-API a FASTAPI Example

A test/psuedo API to use as sample data or test data. Inspired by [FakeResponse.com](http://www.fakeresponse.com/). Documentation can be found at [devsetgo.com/projects/test-api](https://devsetgo.com/projects/test-api).


### Note
- This requires a *Nix environment to run. (Linux, Unix, Windows 10 WSL (unbuntu tested) and I think Mac OS (I don't use a Mac)
- ~~This should be just consider a **beta version** api at this time.~~

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

By commands
~~~~
python3 -m pytest
~~~~
Create coverage badge
~~~~
    coverage-badge -o coverage.svg -f
~~~~
As a Script from app directory
~~~~
./scripts/tests.sh
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

- health
    - [x] GET ***/api/health/***
    - [x] GET ***/api/health/system-info***
    - [x] GET ***/api/health/processes***

## Issues/Bugs

- [ ] None

### TODO
- [X] Setup CI/CD Pipeline for test and deployment
    - [X] [SonarCloud](https://sonarcloud.io)
    - [X] [Travis-CI](https://travis-ci.org)
    - [x] [Github Actions](https://github.com/features/actions) found in .github/workflow/actions
        - [x] tests - matrix run of Python 3.6 and 3.7
        - [x] docker-rc - docker build and push when pull request approved for release-candidate branch (calendar version - rc)
        - [x] docker-master - docker build and push when pull request approved for master branch (calender version and latest)
        - [ ] ensure docker build only happens after pull_request approved and merged into higher branch
- [x] Make [Twelve Factor App](https://12factor.net/) ready

**Application**
- [x] Refactor by endpoint (sample, user, etc..)
- [x] Create tests
    - [x] Minimum of 80%
    - [x] Exception Testing
- [x] Extend API parameters for Users
    - [x] Pagination
    - [x] Number of Items per list returned (Max)
    - [x] Additional Optional for filtering
- [ ] Extend API parameters for ToDo
    - [ ] Pagination
    - [ ] Number of Items per list returned (Max)
    - [ ] Additional Optional for filtering
- [x] Better organization
- [x] Standardize API pattern for versioning
- Access Controls
  - [ ] Add Access controls and signup
  - [ ] Add JWT/Token access
  - [ ] Rate limiting
- [X] Gunicorn with Uvicorn configuration
- [x] Logging (using [Loguru](https://github.com/Delgan/loguru))
- [ ] Build a [cookiecutter](https://github.com/audreyr/cookiecutter) template for future projects similar to the [FastAPI example](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [ ] Add code comments
- [ ] Work on one to many relationshipts
- [ ] Validate userId in ToDo's
- [ ] Work on Connection Pool for SQLite and Postgres for scaling

- Docker
  - [X] Docker-Compose example
    - Configuraton for Traefik (default) and [Jwilder/Nginx-Proxy](https://github.com/jwilder/nginx-proxy) & [JrCs/docker-letsencrypt-nginx-proxy-companion](https://github.com/JrCs/docker-letsencrypt-nginx-proxy-companion)

- Tutorials/Documentation
  - [ ] Basic Overview
  - [ ] Explantion of functions
