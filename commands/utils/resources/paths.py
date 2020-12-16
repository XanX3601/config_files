import pathlib

config_files_repo_path = pathlib.Path(__file__).parent.parent.parent.parent
"""Path: the path to the repository containing this module."""

home_path = pathlib.Path.home()
"""Path: the path to the current user home directory."""

repositories_path = home_path.joinpath("Repositories")
"""Path: the path to the directory where git repositories are stored."""

local_path = home_path.joinpath(".local")
"""Path: the path to the local directory in which everything is installed."""

config_path = home_path.joinpath(".config")
"""Path: the path to the config directory."""

configs_path = config_files_repo_path.joinpath("configs")
"""Path: the path to the directory containing the configs of applications."""

temp_path = pathlib.Path("/tmp")
"""Path: the path to the temporary directory."""

packages_path = home_path.joinpath("Packages")
"""Path: the path to the directory in which package sources are stored."""

resources_dir_paths = [
    repositories_path,
    packages_path,
    local_path,
    config_path,
]
"""list: list of directories used in the installation scripts."""

