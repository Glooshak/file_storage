from pathlib import Path


def obtain_relative_file_path(file_hash: str) -> Path:
    sub_dir_name = file_hash[:2]
    return Path(sub_dir_name) / Path(file_hash)
