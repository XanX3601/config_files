import pathlib
import os

from rich.console import Console

console = Console()

current_path = pathlib.Path(".")
home_path = pathlib.Path.home()
repository_path = home_path.joinpath("repo")
local_path = home_path.joinpath("local")
config_path = home_path.joinpath(".config")
config_bash_path = "$HOME/.config"
bashrc_path = home_path.joinpath(".bashrc")
bashrc_config_path = config_path.joinpath("bashrc")

utils_dirs = [repository_path, local_path, config_path, bashrc_config_path]


def create_utils_dirs():
    """create the main directories"""
    for dir in utils_dirs:
        if not dir.exists():
            os.mkdir(dir)
