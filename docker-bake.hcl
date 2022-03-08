variable "TAG" {
    default = "dev"
}
variable "MULTI_STAGE_TARGET" {
    default = "prod-stage"
}
variable "VUE_APP_API_HOSTNAME" {
    default = "localhost"
}
variable "VUE_APP_API_PREFIX" {
    default = "/api/"
}
variable "VUE_APP_API_PORT" {
    default = "80"
}
variable "VUE_APP_API_PROTOCOL" {
    default = "http"
}
variable "VUE_APP_PUBLIC_PATH" {
    default = "/frontend/"
}
variable "FM_API_PORT" {
    default = "8000"
}

group "default" {
    targets = ["fm_server", "fm_frontend", "fm_api"]
}

target "default" {
    dockerfile = "Dockerfile"
    // platforms = ["linux/amd64", "linux/arm64", "linux/arm/v7", "linux/arm/v6"]
    platforms = ["linux/amd64", "linux/arm64", "linux/arm/v7"]
    pull = true
}

target "fm_server" {
    inherits = ["default"]
    context = "server"
    tags = ["nstoik/fm_server:${TAG}"]
    target = "${MULTI_STAGE_TARGET}"
}

target "fm_frontend" {
    inherits = ["default"]
    context = "frontend"
    tags = ["nstoik/fm_frontend:${TAG}"]
    args = {
        VUE_APP_API_HOSTNAME = "${VUE_APP_API_HOSTNAME}",
        VUE_APP_API_PREFIX = "${VUE_APP_API_PREFIX}",
        VUE_APP_API_PORT = "${VUE_APP_API_PORT}",
        VUE_APP_API_PROTOCOL = "${VUE_APP_API_PROTOCOL}",
        VUE_APP_PUBLIC_PATH = "${VUE_APP_PUBLIC_PATH}"
    }
}

target "fm_api" {
    inherits = ["default"]
    context = "api"
    tags = ["nstoik/fm_api:${TAG}"]
    target = "${MULTI_STAGE_TARGET}"
    args = {
        FM_API_PORT = "${FM_API_PORT}"
    }
}