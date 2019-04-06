# Test-API a FASTAPI Example

A test/psuedo API to use as sample data or test data. Inspired by [FakeResponse.com](http://www.fakeresponse.com/). Documentation can be found at [devsetgo.com/projects/test-api](https://devsetgo.com/projects/test-api).


### Note

This should be just consider a beta app at this time.

## Create Environment

- git clone https://github.com/devsetgo/test-api.git
- python3 -m venv env
- source env/bin/activate
- cd app
- install requirements
  - production: pip3 install -r requirements.txt
  - Development: pip3 install -r requirements/dev.txt
- run it
  - Production: hypercorn main:app  --workers 2 -b 0.0.0.0:5000 --access-log -
  - Development: hypercorn main:app  --reload -b 0.0.0.0:5000 --access-log -
  - Docker: docker pull mikeryan56/test-api:latest

## Issues/Bugs

- [ ] Hypercorn log in Docker does not display anyting (why?)

## TODO

- [ ] Create tests
- [ ] Extend API parameters
- [ ] Better organization
- [ ] Standardize API pattern for versioning
- Access Controls
  - [ ] Add Access controls and signup
  - [ ] Add JWT/Token access
  - [ ] Rate limiting
- [ ] Hypercorn configuration from file (similar to gunicorn?)
- [ ] Logging
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
