FROM node:lts AS build-stage

# the node image already has a node user created with uid and gid 1000

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG USERNAME=node
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG WORKING_DIR=/workspaces/frontend

# add bash history. https://code.visualstudio.com/docs/remote/containers-advanced#_persist-bash-history-between-runs
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && echo $SNIPPET >> "/root/.bashrc" \
    # [Optional] If you have a non-root user
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R $USERNAME /commandhistory \
    && echo $SNIPPET >> "/home/$USERNAME/.bashrc"

# make working directory and change owner
RUN mkdir -p ${WORKING_DIR}/ && \
    chown $USER_UID:$USER_GID ${WORKING_DIR}/

USER $USER_UID:$USER_GID

WORKDIR ${WORKING_DIR}

COPY --chown=${USER_UID}:${USER_GID} package*.json ./

# RUN npm install --include=dev

COPY --chown=${USER_UID}:${USER_GID} ./ $WORKING_DIR/

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

EXPOSE 8080 

CMD ["bin/bash"]