import os
def create_dir(path: str) -> str:
    """Create directory
    """
    if not os.path.exists(path):
        os.makedirs(path)
        return path
    else:return path