FROM python:3.12 as build-stage

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG USERNAME=fm
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG WORKING_DIR=/workspaces/database


RUN pip install -U pip && pip install pipenv && \
    # create new user
    groupadd --gid $USER_GID $USERNAME && \
    useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME && \
    # [Optional] Uncomment the next three lines to add sudo support
    # apt-get install -y sudo && \
    # echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME && \
    # chmod 0440 /etc/sudoers.d/$USERNAME && \
    # make working directory and change owner
    mkdir -p ${WORKING_DIR}/ && \
    chown $USER_UID:$USER_GID ${WORKING_DIR}/

# Change to the newly created user
USER $USER_UID:$USER_GID
COPY --chown=${USER_UID}:${USER_GID} database/. $WORKING_DIR/
COPY --chown=${USER_UID}:${USER_GID} database/Pipfile* database/setup.py $WORKING_DIR/
WORKDIR $WORKING_DIR

# Production deploy steps below
RUN pipenv install --deploy --ignore-pipfile
RUN pipenv run pip install -e .

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

CMD ["pipenv", "run", "fm_database", "update", "database-upgrade", "--revision", "head"]