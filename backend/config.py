import os

MONGODB_DB = os.environ.get("MONGODB_DB", "quatek_web_app")
MONGODB_HOST = os.environ.get("MONGODB_HOST", "127.0.0.1")
MONGODB_PORT = os.environ.get("MONGODB_PORT", 27017)
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1")
SOCKET_HOST = os.environ.get("SOCKET_HOST", "0.0.0.0")
SOCKET_PORT = os.environ.get("SOCKET_PORT", 5858)


# MONGODB_DB = os.environ.get("MONGODB_DB", "quatek_web_app")
# MONGODB_HOST = os.environ.get("MONGODB_HOST", "10.1.6.211")
# MONGODB_PORT = os.environ.get("MONGODB_PORT", 27017)
# REDIS_URL = os.environ.get("REDIS_URL", "redis://10.1.6.211")
# SOCKET_HOST = os.environ.get("SOCKET_HOST", "0.0.0.0")
# SOCKET_PORT = os.environ.get("SOCKET_PORT", 5858)

