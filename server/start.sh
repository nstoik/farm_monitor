#!/bin/bash

# A start up script for the fd_server container.
# This script is called by the Dockerfile when the container is started.
#
# The following environment variables are used:
# - FM_SERVER_WORKER_RUN: A boolean that determines if the worker should be run
# - FM_SERVER_RUN: A boolean that determines if the server should be run

# Only one of the two applications will be run at a time. If both are set to true,
# the server will be run and the worker will be ignored.


# Wait for the database to be ready
echo "Waiting for database to be ready..."
while ! nc -z fm_database 5432; do
  sleep 0.1
done
echo "Database is ready!"

# Run the migrations
echo "Running database migrations..."
pipenv run fm_database update database-upgrade --revision head
echo "Database migrations complete!"

# Check if the FM_SERVER_RUN variable is set and is true
if [ -n "$FM_SERVER_RUN" ] && [ "$FM_SERVER_RUN" = "true" ]; then
  # Start the fm_server in the background
  echo "Starting fm_server..."
  pipenv run fm_server run
  FM_SERVER_RUN_PID=$!

# Check if the FM_SERVER_WORKER_RUN variable is set and is true
elif [ -n "$FM_SERVER_WORKER_RUN" ] && [ "$FM_SERVER_WORKER_RUN" = "true" ]; then
  # Start the fm_server in the background
  echo "Starting fm_server worker..."
  pipenv run fm_server run-worker
  FM_SERVER_WORKER_RUN_PID=$!
fi


# Wait for the server and worker to finish
echo "Waiting for services to finish..."
wait $FM_SERVER_RUN_PID $FM_SERVER_WORKER_RUN_PID

echo "Services finished!"
