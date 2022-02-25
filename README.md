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
docker compose -f docker-compose.yml -f docker-compose.prod.yml  -p fm_prod up -d
```

To bring down the stack run:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml -p fm_prod down
```

# Development
To run the farm_monitor in development, execute the following docker-compose command from the root of the project:

Note the different second file paramater, `-f docker-compose.dev.yml` flag. This is for the development environment.

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -p fm_dev up -d
```



To bring down the stack run:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -p fm_dev down
```

# VS Code Development
To bring the farm_monitor docker stack down in VS Code run the following command:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml -f docker-compose.devcontainer.yml down
```
