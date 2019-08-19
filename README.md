# Test-API a FASTAPI Example
![Calendar Versioning Year Month Day of release](https://img.shields.io/badge/calver-YY.MM.DD-22bfda.svg)

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
    - Some libraries require Python 3.7 or higher (welcome to the edge!)
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


## Issues/Bugs

- [ ] Hypercorn log in Docker does not display anyting (why?)

## TODO

- [x] Refactor by endpoint (sample, user, etc..)
- [ ] Create tests
- [ ] Extend API parameters
- [x] Better organization
- [ ] Standardize API pattern for versioning
- Access Controls
  - [ ] Add Access controls and signup
  - [ ] Add JWT/Token access
  - [ ] Rate limiting
- [ ] Hypercorn configuration from file (similar to gunicorn?)
- [x] Logging (using [Loguru](https://github.com/Delgan/loguru))
- [ ] Setup CI/CD Pipeline for test and deployment
- [ ] Make [Twelve Factor App](https://12factor.net/) ready
- [ ] Build a [cookiecutter](https://github.com/audreyr/cookiecutter) template for future projects similar to the [FastAPI example](https://github.com/tiangolo/full-stack-fastapi-postgresql)
- [ ] Add code comments
- Docker
  - [ ] Docker Stack example
  - [ ] Docker Swarm example
  - [ ] Kubernetes example
- Tutorials/Documentation
  - [ ] Basic Overview
  - [ ] Explantion of functions
