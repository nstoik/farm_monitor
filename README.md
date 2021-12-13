# farm_monitor
 
## Production
To run the farm_monitor in production, execute the following docker-compose command from the root of the project:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

To bring down the stack run:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml down
```

## Development
To run the farm_monitor in development, execute the following docker-compose command from the root of the project:

Note the different second file paramater, `-f docker-compose.dev.yml` flag. This is for the development environment.

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```



To bring down the stack run:

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml down
```