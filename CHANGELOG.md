# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).
 
## [Unreleased] - yyyy-mm-dd
 
Here we write upgrading notes for.
 
### Added
- [PROJECTNAME-XXXX](http://tickets.projectname.com/browse/PROJECTNAME-XXXX)
  MINOR Ticket title goes here.
- [PROJECTNAME-YYYY](http://tickets.projectname.com/browse/PROJECTNAME-YYYY)
  PATCH Ticket title goes here.
### Changed

### Fixed

## Unreleased - [v0.3.4](https://github.com/nstoik/farm_device/releases/tag/v0.3.4) - 2024-mm-dd
 
### Update Instructions
- Update the `TAG` variable in the `.env` file to `v0.3.4`. 

Then execute the following to pull and run the containers:
```bash
> docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env -p fd_prod down
> docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env -p fd_prod pull
> docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env -p fd_prod up -d
```

### Added
- `CHANGELOG.md` file to track changes to the project and added documentation on how to release new versions.

### Changed
- Removed typescript vue plugin from the frontend sub repo.
- Docker contexts for the container build process.

### Fixed

## [v0.3.3](https://github.com/nstoik/farm_monitor/releases/tag/v0.3.3) - 2024-03-24

### Update Instructions
- Update the `TAG` variable in the `.env` file to `v0.3.3`. 
- Update the `VUE_APP_*` environment variables in the `.env` file to `VITE_*`.

Then execute the following to pull and run the containers:
```bash
> docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env -p fm_prod down
> docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env -p fm_prod pull
> docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env -p fm_prod up -d
```

### Added

### Changed
- Bring all dependencies up to date.
- Changed to Vite for the frontend sub repo.
- **Breaking:** Changed frontend environment variable prefix from `VUE_APP_` to `VITE_`.

### Fixed
