# Test-API a FASTAPI Example
A test/psuedo API to use as sample data or test data. Inspired by FakeResponse.com

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


### ToDO