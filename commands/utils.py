import pathlib
import os

from rich.console import Console

console = Console()

current_path = pathlib.Path(".")
home_path = pathlib.Path.home()
repository_path = home_path.joinpath("repo")
local_path = home_path.joinpath("local")
config_path = home_path.joinpath(".config")
configs_path = current_path.joinpath("configs")
config_bash_path = "$HOME/.config"
bashrc_path = home_path.joinpath(".bashrc")
bashrc_config_path = config_path.joinpath("bashrc")
temp_path = pathlib.Path("/tmp")
package_path = home_path.joinpath("package")

utils_dirs = [
    repository_path,
    package_path,
    local_path,
    config_path,
    bashrc_config_path,
]


def create_utils_dirs():
    """create the main directories"""
    for dir in utils_dirs:
        if not dir.exists():
            console.print('Creating directory "{}"...'.format(dir), end="")
            os.mkdir(dir)
            console.print("[bold green]Done![/]")
