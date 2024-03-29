#-------------------------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See https://go.microsoft.com/fwlink/?linkid=2090316 for license information.
#-------------------------------------------------------------------------------------------------------------

FROM python:3.12 as dev-stage

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG USERNAME=fm
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG WORKING_DIR=/workspaces/server

# Configure apt and install packages
RUN apt-get update && \
    apt-get -yqq install --no-install-recommends apt-utils dialog apt-transport-https locales 2>&1 && \
    #
    # Verify git, process tools, lsb-release (common in install instructions for CLIs) installed
    apt-get -yqq install git procps lsb-release netcat-traditional && \
    # Clean up
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/lib/apt/lists/*

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

# add bash history. https://code.visualstudio.com/docs/remote/containers-advanced#_persist-bash-history-between-runs
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo $SNIPPET >> "/root/.bashrc" \
    # [Optional] If you have a non-root user
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory \
    && echo $SNIPPET >> "/home/$USERNAME/.bashrc"

# Change to the newly created user
USER $USER_UID:$USER_GID
COPY --chown=${USER_UID}:${USER_GID} server/. $WORKING_DIR/
COPY --chown=${USER_UID}:${USER_GID} server/Pipfile* server/setup.py $WORKING_DIR/
WORKDIR $WORKING_DIR

# Set up the dev environment
# (this is run manually inside the container instead for dev)
# RUN pipenv install --dev

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

EXPOSE 5554

CMD ["/bin/bash"]