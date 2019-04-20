# Test-API a FASTAPI Example

A test/psuedo API to use as sample data or test data. Inspired by [FakeResponse.com](http://www.fakeresponse.com/). Documentation can be found at [devsetgo.com/projects/test-api](https://devsetgo.com/projects/test-api).


### Note
- This requires a *Nix environment to run. (Linux, Unix, Windows 10 WSL (unbuntu tested) and I think Mac OS (don't use it)
- This should be just consider a beta app at this time.

## Create Environment

- git clone https://github.com/devsetgo/test-api.git
- python3.7 -m venv env
- source env/bin/activate
- cd app
- install requirements
  - Notes:
    - Some libraries require Python 3.7 or higher (welcome to the edge!)
      - Note: I am using [Ubuntu via WSL](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
      - Upgrading (adding) [Python 3.7 to Ubuntu](https://jcutrer.com/linux/upgrade-python37-ubuntu1810) and setting it as the default for Python3
      - Upgrading [Python3 and install venv](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart)
    - You may need to upgrade pip and setuptools first (pip3 install --upgrade pip setuptools)
  - production: pip3 install -r requirements.txt
  - Development: pip3 install -r requirements/dev.txt
- run it
  - Production: hypercorn app:app  --workers 2 -b 0.0.0.0:5000 --access-log -
  - Development: hypercorn app:app  --reload -b 0.0.0.0:5000 --access-log -
  - Docker: docker pull mikeryan56/test-api:latest

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
