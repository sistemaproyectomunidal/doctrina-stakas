import os

def get_secret(name: str):
    val = os.getenv(name)
    if not val:
        raise EnvironmentError(f"Secret {name} not set in environment")
    return val
