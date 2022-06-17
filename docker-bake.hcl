variable "TAG" {
    default = "dev"
}
variable "TRAEFIK_DOMAIN" {
    default = "localhost"
}
variable "MULTI_STAGE_TARGET" {
    default = "prod-stage"
}
variable "VUE_APP_API_HOSTNAME" {
    default = "${TRAEFIK_DOMAIN}"
}
variable "VUE_APP_API_PREFIX" {
    default = "/api"
}
variable "VUE_APP_API_PORT" {
    default = "443"
}
variable "VUE_APP_API_PROTOCOL" {
    default = "https"
}
variable "VUE_APP_PUBLIC_PATH" {
    default = "/frontend/"
}

group "default" {
    targets = ["fm_server", "fm_frontend", "fm_api", "fm_flower"]
}

target "default" {
    dockerfile = "Dockerfile"
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
    tags = ["nstoik/fm_frontend:${TAG}", "nstoik/fm_frontend:${TAG}-${TRAEFIK_DOMAIN}"]
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
}

target "fm_flower" {
    inherits = ["default"]
    context = "flower"
    tags = ["nstoik/fm_flower:${TAG}"]
}