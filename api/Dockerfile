# Add the pyton parts
FROM python:3.12 as build-stage

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG USERNAME=fm
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG WORKING_DIR=/workspaces/api
ARG DATABASE_DIR=/workspaces/database

RUN pip install -U pip && pip install pipenv && \
    # create new user
    groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    # [Optional] Uncomment the next three lines to add sudo support
    # apt-get install -y sudo && \
    # echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    # chmod 0440 /etc/sudoers.d/$USERNAME && \
    # make working directory and change owner
    mkdir -p $WORKING_DIR/ && \
    mkdir -p $DATABASE_DIR/ && \
    chown $USER_UID:$USER_GID $WORKING_DIR/ $DATABASE_DIR/ && \
    # create directory for logs and change owner
    mkdir /logs/ && \
    chown $USER_UID:$USER_GID /logs/

# Change to the newly created user
USER $USER_UID:$USER_GID

# Copy the Pipfile and Pipfile.lock to the working directory
COPY --chown=${USER_UID}:${USER_GID} api/Pipfile* api/setup.py $WORKING_DIR/
# Copy the database subfolder
COPY --chown=${USER_UID}:${USER_GID} database/. $DATABASE_DIR/

WORKDIR $WORKING_DIR
RUN pipenv install --deploy --ignore-pipfile

# dev stage steps below
FROM build-stage as dev-stage

ARG FM_API_PORT

COPY --chown=${USER_UID}:${USER_GID} api/. $WORKING_DIR/
RUN pipenv run pip install -e .

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

CMD pipenv run fm_api flask-cli run --host=0.0.0.0 --port=$FM_API_PORT

# prod stage steps below. Similiar as the dev stage, but we copy the venv from
# the build stage to the prod stage. (no git in the slim version of this docker base image)
FROM python:3.12-slim AS prod-stage
# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG USERNAME=fm
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG WORKING_DIR=/workspaces/api

ARG FM_API_PORT

# install libpq-dev for python postgres support
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip && pip install pipenv && \
    # create new user
    groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    # [Optional] Uncomment the next three lines to add sudo support
    # apt-get install -y sudo && \
    # echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    # chmod 0440 /etc/sudoers.d/$USERNAME && \
    # make working directory and change owner
    mkdir -p $WORKING_DIR/ && \
    chown $USER_UID:$USER_GID $WORKING_DIR/ && \
    # create directory for logs and change owner
    mkdir /logs/ && \
    chown $USER_UID:$USER_GID /logs/

# Change to the newly created user
USER $USER_UID:$USER_GID
COPY --chown=${USER_UID}:${USER_GID} api/. $WORKING_DIR/
# here we copy the venv from the dev stage to the prod stage
COPY --from=build-stage /home/${USERNAME}/.local/share /home/${USERNAME}/.local/share


WORKDIR $WORKING_DIR
RUN pipenv run pip install -e .

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

CMD pipenv run gunicorn fm_api.wsgi:app --access-logfile '-' --bind 0.0.0.0:$FM_API_PORT
