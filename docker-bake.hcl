variable "TAGS" {
    default = "dev"
}
variable "TRAEFIK_DOMAINS" {
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
    platforms = ["linux/amd64", "linux/arm64", "linux/arm/v7"]
    context = "."
    pull = true
}

target "fm_server" {
    inherits = ["default"]
    dockerfile = "server/Dockerfile"
    tags = [for tag in split(",", "${TAGS}"): "nstoik/fm_server:${tag}"]
    target = "${MULTI_STAGE_TARGET}"
}

target "fm_api" {
    inherits = ["default"]
    dockerfile = "api/Dockerfile"
    tags = [for tag in split(",", "${TAGS}"): "nstoik/fm_api:${tag}"]
    target = "${MULTI_STAGE_TARGET}"
}

target "fm_flower" {
    inherits = ["default"]
    dockerfile = "flower/Dockerfile"
    tags = [for tag in split(",", "${TAGS}"): "nstoik/fm_flower:${tag}"]
}

target "fm_frontend" {
    inherits = ["default"]
    dockerfile = "frontend/Dockerfile"
    matrix = {
        domain = split(",", "${TRAEFIK_DOMAINS}")
    }
    name = replace("frontend-${domain}", ".", "-")
    tags = concat(
        [for tag in split(",", "${TAGS}"): "nstoik/fm_frontend:${tag}"],
        [for tag in split(",", "${TAGS}"): "nstoik/fm_frontend:${tag}-${domain}"]
    )
    args = {
        VITE_API_HOSTNAME = "${domain}",
        VITE_API_PREFIX = "${VITE_API_PREFIX}",
        VITE_API_PORT = "${VITE_API_PORT}",
        VITE_API_PROTOCOL = "${VITE_API_PROTOCOL}",
        VITE_PUBLIC_PATH = "${VITE_PUBLIC_PATH}"
    }
}
