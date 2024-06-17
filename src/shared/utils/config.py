def format_debug(debug: str) -> bool:
    return debug.lower() == 'true'


def format_allowed_hosts(allowed_hosts: str) -> [str]:
    return allowed_hosts.split(',')[1:-1]


def format_cors_allowed_origins(cors_allowed_origins: str) -> [str]:
    return cors_allowed_origins.split(',')[1:-1]
