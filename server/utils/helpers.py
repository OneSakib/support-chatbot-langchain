import hashlib


def generate_project_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()
