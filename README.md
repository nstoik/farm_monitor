# farm_monitor
Main documentation for the farm_monitor package.

# env variables
There is a set of environment variables that can be used to configure the application. In the GitHub repository, an example configuration file is available in the root directory as `.env.example`.

There are SECRET variables and there are CONFIGURATION variables.

To create random secret keys for env variables (eg. `FM_API_SECRET`), run the following command, and then copy and paste the output into the `.env` file:

``` 
$ openssl rand -hex 32
```

This file has a `FM_GENERAL_CONFIG` variable at the top that controls the general configuration of the different mono repos. Hint: change this variable between 'dev', 'prod', or 'test'.

The majority of the docker commands use the `.env` file by default to configure the containers. Edit the `.env` file as needed for the specific environment (including setting SECRET and TOKEN variables).

The `docker buildx bake` commands use configuration variables in the `docker-bake.hcl` file. These can be overridden as shown below when building images using `docker buildx bake`.

The containers use environment variables when the stack is brought up (environment variables). Some containers require build-args to be applied at build time instead. Currently, the two containers that have build-args are `fm_frontend` and `fm_api`.

Each monorepo can have its own set of environment variables if applicable. This are used for local development and testing. An example configuration file is available in the monorepo directory as `.env.example`.
 
# Production
**Make sure to set the appropriate environment variables**

## Installing Docker and Docker Compose

To install Docker and Docker Compose, follow the steps from the [Docker Webpage](https://docs.docker.com/engine/install/ubuntu/#install-docker-engine)


## Using Docker Compose

To run the farm_monitor in production, execute the following docker-compose command from the root of the project:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml  --env-file .env -p fm_prod up -d --no-build
```

To bring down the stack run:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file .env -p fm_prod down
```

# Development
**Make sure to set the appropriate environment variables**

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
VS Code automatically builds the required containers when you launch into a remote container. This uses the `docker-compose.devcontainer.yml` overrides.

In order to speed up the container build time, python dependencies are not installed in the containers during the build process. Instead, they need to
be installed manually. To do this, open a terminal in VS Code and run the following command inside the container as needed:

```bash
  cd [module] (eg. 'api', 'server', 'database')
  pipenv install --dev
  pipenv shell
```

To bring the farm_monitor docker stack down in VS Code run the following command:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.devcontainer.yml down
```

# Building Docker Containers
There are multiple options for building the docker containers. 

## Build single platform container
To build a single docker container for a single platform, execute the following command:
```bash
docker build {PATH} --file {PATH}/Dockerfile --no-cache --pull --build-arg {ENV NAME}={ENV VALUE} --tag nstoik/{module}:{tag}  --target {target}
```
An example command for building the fm_frontend container version 1.0.0-rc is:
```bash
docker build . --file frontend/Dockerfile --no-cache --pull --build-arg VITE_API_HOSTNAME=localhost --build-arg VITE_PUBLIC_PATH=/frontend/ --tag nstoik/fm_frontend:1.0.0-rc
```
- {PATH} is the context of the build
- --build-arg is optional and can pass in environment variables to docker build. It can be repeated for multiple variables.
    - {ENV NAME} is the name of the environment variable
    - {ENV VALUE} is the value of the environment variable
- {module} is the name of the module
- {tag} is the tag of the docker image
- {target} is the target to build

## Bulid multiple containers for a single platform
To build multiple docker containers for a single platform, execute the following command:
```bash
docker compose --file {docker-compose file} --env-file {env file} build --no-cache --pull
```
An example command for building all containers for prod is below. Upddate the `FM_TAG` variable in the environment file to the tag you want to build.
```bash
docker compose --file docker-compose.yml --file docker-compose.prod.yml --env-file .env build --no-cache --pull
```

To push the containers to the docker hub, execute the following command:
```bash
docker compose --file {docker-compose file} --env-file {env file} push
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

Bake all the containers. In the example below, the TAG variable is set to the tag you want to build.
```bash
TAG=0.1 docker buildx bake --builder fm_buildx --file docker-bake.hcl --push
```

To build the frontend container with a specific Traefik domain of `fm1.farmmonitor.ca`, execute the following command:
```bash
TAG=0.1 TRAEFIK_DOMAINS=fm1.farmmonitor.ca docker buildx bake --builder fm_buildx --file docker-bake.hcl fm_frontend --push
```
**Note** Overwrite variables defined in the `docker-bake.hcl` file by specifying them as arguments to the command. Any required `ARG` in the docker files need to be specified in the `docker-bake.hcl` file.

The list of available variables are:
- TAG: The tag of the docker image to build. Defaults to "dev"
- MULTI_STAGE_TARGET: The target to build. Defaults to "prod-stage"
- TRAEFIK_DOMAINS: The domain name of the traefik service. Defaults to "localhost". Can be a comma separated list of domains to build multiple containers with different domains specified.
- VITE_API_PREFIX: defaults to "/api"
- VITE_API_PORT: The port the frontend connects to. Defaults to "443"
- VITE_API_PROTOCOL: The protocol the API is exposed on. Defaults to "https"
- VITE_PUBLIC_PATH: The public path of the frontend. Defaults to "/frontend/"

A few additional comments on the `docker-bake.hcl` file:
- --print is optional and will print the configuration of the builder
- --push will push the built images to the registry
- --load is optional and will load the image into docker
  - When using --load, only a sinle platform can be specified. An example of overriding the platform for 'linux/amd64' is `--set default.platform=linux/amd64`