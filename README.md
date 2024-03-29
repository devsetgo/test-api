Python:
![image](https://img.shields.io/badge/calver-YYYY.MM.DD-22bfda.svg "CalVer")
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)

CI/CD Pipeline:

[![Actions Status](https://github.com/devsetgo/test-api/workflows/Run%20Tests/badge.svg)](https://github.com/devsetgo/test-api/actions)
[![Publish Docker image](https://github.com/devsetgo/test-api/actions/workflows/docker-latest.yml/badge.svg)](https://github.com/devsetgo/test-api/actions/workflows/docker-latest.yml)
![Docker Image](https://img.shields.io/docker/pulls/mikeryan56/test-api)

SonarCloud:

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=coverage)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=ncloc)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=security_rating)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=alert_status)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_test-api&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=devsetgo_test-api)


# Test-API a FASTAPI Example

A test/psuedo API to use as sample data or test data. Inspired by [FakeResponse.com](http://www.fakeresponse.com/). Documentation can be found at [devsetgo.com/projects/test-api](https://devsetgo.com/projects/test-api).


### Note
- This requires a *Nix environment to run. (Linux, Unix, Windows 10 WSL (unbuntu tested) and I think Mac OS (I don't use a Mac)
- It should be considered only an example and just something to learn from.

## Create Environment

- Copy the repository
  ~~~~
  git clone https://github.com/devsetgo/test-api.git
  python-3 -m venv env
  source env/bin/activate
  cd app
  ~~~~

- Notes:
    - Everything has been test on Python 3.11. Should run on 3.7 - 3.11.
      - Note: I am using [Ubuntu via WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
      - Upgrading [Python3 and install venv](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart)
    - You may need to upgrade pip and setuptools first (pip3 install --upgrade pip setuptools)
- Install requirements
  ~~~~
  from src folder: ./scripts/install.sh
  Production: pip3 install -r requirements.txt
  Development: pip3 install -r requirements/dev.txt
  ~~~~

Setup: Copy .env_sample to .env and set configuration as desired.
~~~~bash
$ cp .env_example .env
~~~~
.env_sample file
~~~~
# # This is used to determin if .env or other external config is used. True is for a .env file and false for docker enviroment
# # option: dotenv, docker
USE_ENV='dotenv'

# Application information
TITLE="Test API"
DESCRIPTION="Test APIs for tools and other examples"
APP_VERSION='One'
OWNER='Your Name'
WEBSITE='https://your.domain.com/support'

# Demo settings
CREATE_SAMPLE_DATA=true
NUMBER_TASKS=10
NUMBER_USERS=10
NUMBER_GROUPS=10

# Cofigurations
HOST_DOMAIN='https://your.domain.com'
#prd for production or 'dev' for development
RELEASE_ENV='dev'
# Turn HTTPS Middleware on (True) or off (False)
HTTPS_ON=false
# Turn on Prometheus endpoint
PROMETHEUS_ON=true

# data base URI
SQLALCHEMY_DATABASE_URI='sqlite:///sqlite_db/api.db'
# Loguru settings
LOGURU_RETENTION='10 days'
LOGURU_ROTATION='100 MB'
# Values NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGURU_LOGGING_LEVEL='INFO'
# Workers - Set to 1 for CPUs x 2 + 1
WORKERS=4
# Leave intact for license
CREATED_BY='Mike Ryan'
LICENSE_TYPE='MIT'
LICENSE_LINK='https://github.com/devsetgo/test-api/blob/master/LICENSE'

~~~~

Start the app
~~~~
FROM SCR
    Development"
        ./scripts/dev_run.sh
    Production:
        ./scripts/prd_run.sh

UVICORN
    Development:
        uvicorn main:app --port 5000 --reload
        python3 main.py (running Uvicorn from Code - no reload)

    Production:
        uvicorn main:app --port 5000 --workers 2
        python3 main.py (running Uvicorn from code)
        gunicorn -c gunicorn_cfg.py main:app
        # Note: gunicorn is the config for the dockerfile

Docker
    Docker: docker pull mikeryan56/test-api:latest
~~~~

### Run Tests
By commands

SchemaThesis
~~~~
st run --workers 10 --fixups fast_api --request-timeout 21000 --max-response-time 21000 --max-failures 2 --hypothesis-deadline 2000 --junit-xml junit.xml http://127.0.0.1:5000/openapi.json

st run --workers 6 --fixups fast_api --request-timeout 21000 --max-response-time 21000 --max-failures 2 --junit-xml junit.xml http://127.0.0.1:5000/openapi.json
~~~~
~~~~
./scripts/tests.sh
~~~~
~~~~
python3 -m pytest
~~~~
Create coverage badge
~~~~
    coverage-badge -o coverage.svg -f
~~~~
As a Script from src directory
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

- groups
    - [x] GET ***/api/v1/groups/list***
    - [x] GET ***/api/v1/groups/list/count***
    - [x] PUT ***/api/v1/groups/state***
    - [x] POST ***/api/v1/groups/create***
    - [x] GET ***/api/v1/groups/group***
    - [x] POST ***/api/v1/groups/user/create***
    - [x] DELETE ***/api/v1/groups/user/delete***

- textblob
    - [x] POST ***/api/v1/textblob/sentiment***
    - [x] POST ***/api/v1/textblob/spellcheck***

- todos
    - [x] GET ***/api/v1/todo/list***
    - [x] GET ***/api/v1/todo/list/count***
    - [x] GET ***/api/v1/todo/list/{todo_id}***
    - [x] DELETE ***/api/v1/todo/list/{todo_id}***
    - [x] PUT ***/api/v1/todo/list/{todo_id}***
    - [x] POST ***/api/v1/todo/create/***

- users
    - [x] GET ***/api/v1/users/list***
    - [x] GET ***/api/v1/users/list/count***
    - [x] GET ***/api/v1/users/list/{user_id}***
    - [x] DELETE ***/api/v1/users/list/{user_id}***
    - [x] PUT ***/api/v1/users/list/{user_id}***
    - [x] POST ***/api/v1/users/create/***
    - [x] POST ***/api/v1/users/check-pwd/***

- tools
    - [x] POST ***/api/v1/tools/convert-to/xml***
    - [x] POST ***/api/v1/tools/convert-to/json***

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
    - ~~[X] [Travis-CI](https://travis-ci.org)~~ ***replaced by Github Actions***
    - [X] [SonarCloud](https://sonarcloud.io)
    - [x] [Github Actions](https://github.com/features/actions) found in .github/workflow/actions
        - [x] docker-rc - docker build and push when pull request approved for release-candidate branch (calendar version - rc)
        - [x] docker-master - docker build and push when pull request approved for master branch (calender version and latest)
        - [x] ensure docker build only happens after pull_request approved and merged into higher branch
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
- [ ] Extend Tools API
    - [ ] Text Conversion
        - [x] XML to JSON (required to be valid XML)
        - [ ] JSON to XML (required to be valid XML)
    - [ ] Text Functions
        - [ ] Language of text

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
