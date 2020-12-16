
import click

from .utils.resources import repositories_path, local_path, configs_path, config_path, console
from .utils.git import clone_repository, update_repository, NotAGitRepo
from .utils.files import LocationExists, copy, create_directory
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.make import make, make_install

nvim_name = "neovim"
nvim_repo_link = "https://github.com/neovim/neovim.git"
nvim_repo_path = repositories_path.joinpath("neovim")
nvim_install_path = local_path
nvim_build_path = nvim_repo_path.joinpath("build")
nvim_init_path = configs_path.joinpath("neovim/init.vim")
nvim_config_path = config_path.joinpath("nvim")


@click.group()
def neovim():
    """neovim commmands group."""
    pass


@neovim.command()
def install():
    """install neovim locally."""
    # clone repository
    try:
        clone_repository(nvim_repo_link, nvim_repo_path, nvim_name)
    except LocationExists as exception:
        pass

    # update local repository
    try:
        update_repository(nvim_repo_path, nvim_name)
    except NotAGitRepo as exception:
        print_msg_titled("Error while updating {} repository".format(nvim_name), str(exception))
        
    # make 
    returncode, stdout, stderr = make(nvim_repo_path, ["CMAKE_INSTALL_PREFIX={}".format(nvim_install_path)], nvim_name)
    if returncode != 0:
        print_stdoutputs("[bold red]Error while compiling {}[/]".format(nvim_name), stdout, stderr)

    # make install
    returncode, stdout, stderr = make_install(nvim_repo_path, [], nvim_name)
    if returncode != 0:
        print_stdoutputs("[bold red]Error while compiling {}[/]".format(nvim_name), stdout, stderr)

    # install nvim.init
    if not nvim_config_path.exists():
        create_directory(nvim_config_path)

    copy(nvim_init_path, nvim_config_path, "{} {}".format(nvim_name, nvim_init_path.name))

    console.print("[bold green]{} has been installed with success[/]".format(nvim_name))

