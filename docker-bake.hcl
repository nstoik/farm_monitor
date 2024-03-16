variable "TAG" {
    default = "dev"
}
variable "TRAEFIK_DOMAIN" {
    default = "localhost"
}
variable "MULTI_STAGE_TARGET" {
    default = "prod-stage"
}
variable "VITE_API_PREFIX" {
    default = "/api"
}
variable "VITE_API_PORT" {
    default = "443"
}
variable "VITE_API_PROTOCOL" {
    default = "https"
}
variable "VITE_PUBLIC_PATH" {
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

target "fm_frontend" {
    inherits = ["default"]
    context = "frontend"
    matrix = {
        domain = split(",", "${TRAEFIK_DOMAIN}")
    }
    name = "frontend-${domain}"
    tags = ["nstoik/fm_frontend:${TAG}", "nstoik/fm_frontend:${TAG}-${domain}"]
    args = {
        VITE_API_HOSTNAME = "${domain}",
        VITE_API_PREFIX = "${VITE_API_PREFIX}",
        VITE_API_PORT = "${VITE_API_PORT}",
        VITE_API_PROTOCOL = "${VITE_API_PROTOCOL}",
        VITE_PUBLIC_PATH = "${VITE_PUBLIC_PATH}"
    }
}
