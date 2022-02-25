# farm_monitor
Main documentation for the farm_monitor package.

# env variables
There is a set of environment variables that can be used to configure the application. In the GitHub repository, an example configuration file is available in the root directory as `.env.example`.

This file has a `FM_GENERAL_CONFIG` variable at the top that controls the general configuration of the different mono repos. Hint: change this variable between 'dev', 'prod', or 'test'.

By default the `.env` file is loaded by docker compose in the commands below.

Each monorepo can have its own set of environment variables if applicable. This are used for local development and testing. An example configuration file is available in the monorepo directory as `.env.example`.
 
# Production
To run the farm_monitor in production, execute the following docker-compose command from the root of the project:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml  --env-file .env -p fm_prod up -d --no-build
```

To bring down the stack run:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env -p fm_prod down
```

# Development
To run the farm_monitor in development, execute the following docker-compose command from the root of the project:

Note the different second file paramater, `-f docker-compose.dev.yml` flag. This is for the development environment.

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env -p fm_dev up -d
```



To bring down the stack run:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml --env-file .env -p fm_dev down
```

# VS Code Development
To bring the farm_monitor docker stack down in VS Code run the following command:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.devcontainer.yml down
```

# Building Docker Containers
There are multiple options for building the docker containers. 

## Build single platform container
To build a single docker container for a single platform, execute the following command:
```bash
docker build {PATH} --file {PATH}/Dockerfile --no-cache --pull --build-arg {ENV NAME}={ENV VALUE} --tag nstoik/{module}:{tag}
```
An example command for building the fm_frontend container version 1.0.0-rc is:
```bash
docker build frontend --file frontend/Dockerfile --no-cache --pull --build-arg VUE_APP_API_HOSTNAME=localhost --build-arg VUE_APP_PUBLIC_PATH=/frontend/ --tag nstoik/fm_frontend:1.0.0-rc
```
- {PATH} is the submodule path
- --build-arg is optional and can pass in environment variables to docker build. It can be repeated for multiple variables.
    - {ENV NAME} is the name of the environment variable
    - {ENV VALUE} is the value of the environment variable
- {module} is the name of the module
- {tag} is the tag of the docker image

## Bulid multiple containers for a single platform
To build multiple docker containers for a single platform, execute the following command:
```bash
docker compose --file {docker-compose file} --env-file {env file} build --no-cache --pull
```
An example command for building all containers is below. Upddate the `FM_TAG` variable in the environment file to the tag you want to build.
```bash
docker compose --file docker-compose.yml --env-file .env build --no-cache --pull
```
- {docker-compose file} is the docker-compose file
- {env file} is the .env file
## Building multi platform containers and pushing to a registry
First setup the prequisites. Configure buildx tools
```bash
docker buildx create --name fm_buildx
``` 
To list the available builders run:
```bash
docker buildx ls
```

Bake all the containers
```bash
TAG={docker-tag} docker buildx bake --builder fm_buildx --file docker-bake.hcl --push
```
You can overwrite variables defined in the `docker-bake.hcl` file by specifying them as arguments to the command.
- {docker-tag} is the tag you want to build
- print is optional and will print the configuration of the builder
- push will push the built images to the registry