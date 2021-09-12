FROM node:16 AS build-stage

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ARG WORKING_DIR=/workspaces/frontend

RUN npm install -g @vue/cli

WORKDIR $WORKING_DIR

COPY package*.json ./

RUN npm install

COPY ./ $WORKING_DIR/

RUN npm run build

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=

FROM nginx:latest

COPY --from=build-stage $WORKING_DIR/dist/ /usr/share/nginx/html

COPY --from=build-stage /nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
