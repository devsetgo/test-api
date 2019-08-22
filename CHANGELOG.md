# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Todo
- [ ] Add Testing
- [ ] Create cookiecutter from template
- [ ] Work on one to many relationshipts
- [ ] Validate userId in ToDo's
- [ ] Work on Connection Pool for SQLite and Postgres for scaling

## [Unreleased]
- websockets (working on it)


## [19.4.20-beta-1] - 2019-04-20
### Added
- routers for todo, users, and silly
- .env file update
- Logging via Loguru

### Changed
- Refactor application
- Changed list to database (SQLite or Postgres)

### Removed
- a lot... due to refactoring
- Removed list for todos
- Some of the Silly endpoints to limit to just list or one user generation

## [19.4.6-beta-1] - 2019-04-06
### Added
- initial commit
- building base frame of project
  - 'User' random data (extension of FastAPI example)
    - Random user contact information
  - 'Item' little change from FastAPI example
  - 'Sample' Generates randomized data
    - can set a delay in seconds (0 -10) as a parameter
    - list can generate from 1 to 1000

### Changed
- Nothing, since it is an initial commit

### Removed
- Nothing, since it is an initial commit
