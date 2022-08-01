FROM node:16 AS build-stage

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG WORKING_DIR=/workspaces/frontend

ARG VUE_APP_API_HOSTNAME
ARG VUE_APP_API_PREFIX=/api
ARG VUE_APP_API_PORT=80
ARG VUE_APP_API_PROTOCOL=http
ARG VUE_APP_PUBLIC_PATH=/

RUN npm install -g @vue/cli

WORKDIR $WORKING_DIR

COPY package*.json ./

RUN npm install

COPY ./ $WORKING_DIR/

RUN npm run build

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

FROM nginx:latest
ARG WORKING_DIR=/workspaces/frontend

# remove all existing nginx html files
RUN rm -rf /usr/share/nginx/html/*

# copy the build output to the nginx html directory
COPY --from=build-stage $WORKING_DIR/dist/ /usr/share/nginx/html

# copy the nginx configuration files
COPY --from=build-stage $WORKING_DIR/nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage $WORKING_DIR/nginx-default-farmmonitor-frontend.conf /etc/nginx/extra-conf.d/default-farmmonitor-frontend.conf
