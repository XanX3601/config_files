import click

from .utils.commands import call_command, is_callable
from .utils.files import LocationExists, copy, create_directory, download_file
from .utils.git import NotAGitRepo, clone_repository, update_repository
from .utils.make import make, make_install
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.resources import (config_path, configs_path, console, local_path,
                              repositories_path)

from .automake import install as automake_install
from .libtool import install as libtool_install

nvim_name = "neovim"
nvim_homepage = "https://neovim.io/"
nvim_repo_link = "https://github.com/neovim/neovim.git"
nvim_repo_path = repositories_path.joinpath("neovim")
nvim_install_path = local_path
nvim_build_path = nvim_repo_path.joinpath("build")
nvim_init_path = configs_path.joinpath("neovim/init.vim")
nvim_config_path = config_path.joinpath("nvim")
vimplug_link = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"


@click.group()
def neovim():
    """neovim commmands group."""
    pass


@neovim.command()
def info():
    """print info on nvim."""
    print_msg_titled(
        "{}".format(nvim_name),
        "home page: {}".format(nvim_homepage),
    )


@neovim.command()
@click.option('--with-dependencies', is_flag=True, help="Install with dependencies")
@click.pass_context
def install(ctx, with_dependencies):
    """install neovim locally."""
    # handle dependencies
    if with_dependencies:
        ctx.invoke(automake_install, with_dependencies=with_dependencies)
        ctx.invoke(libtool_install)

    # clone repository
    try:
        clone_repository(nvim_repo_link, nvim_repo_path, nvim_name)
    except LocationExists as exception:
        pass

    # update local repository
    try:
        update_repository(nvim_repo_path, nvim_name)
    except NotAGitRepo as exception:
        print_msg_titled(
            "[bold red]Error while updating {} repository[/]".format(nvim_name),
            str(exception),
        )

    # make
    returncode, stdout, stderr = make(
        nvim_repo_path, ["CMAKE_INSTALL_PREFIX={}".format(nvim_install_path)], nvim_name
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while compiling {}[/]".format(nvim_name), stdout, stderr
        )
        exit(1)

    # make install
    returncode, stdout, stderr = make_install(nvim_repo_path, [], nvim_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while compiling {}[/]".format(nvim_name), stdout, stderr
        )
        exit(1)

    # installing vimplug
    share_path = local_path.joinpath("share")
    if not share_path.exists():
        create_directory(share_path)

    nvim_share_path = share_path.joinpath("nvim")
    if not nvim_share_path.exists():
        create_directory(nvim_share_path)

    site_path = nvim_share_path.joinpath("site")
    if not site_path.exists():
        create_directory(site_path)

    autoload_path = site_path.joinpath("autoload")
    if not autoload_path.exists():
        create_directory(autoload_path)

    plug_vim_path = autoload_path.joinpath("plug.vim")

    download_file(vimplug_link, plug_vim_path, "vimplug")

    # install nvim.init
    if not nvim_config_path.exists():
        create_directory(nvim_config_path)

    copy(
        nvim_init_path, nvim_config_path, "{} {}".format(nvim_name, nvim_init_path.name)
    )

    # call PlugInstall from vimplug
    args = ["nvim", "-E", "+PlugInstall", "+qall"]
    returncode, stdout, stderr = call_command(args, "PlugInstall")

    if returncode != 0 and returncode != 1:
        print_stdoutputs(
            "[bold red]Error while installing neovim plugin[/]", stdout, stderr
        )
        exit(1)

    # installing coc plugins
    # not currently working
    """
    if not is_callable("node"):
        print_msg_titled("[bold red]Error installing coc extensions[/]", "node is not callable. Please install it and then retry.")
        exit(1)

    args = ["nvim", "+\"CocInstall coc-pyright\"", "+qall"]
    returncode, stdout, stderr = call_command(args, "CocInstall")

    if returncode != 0:
        print_stdoutputs("[bold red]Error while installing coc nvim plugins[/]", stdout, stderr)
        exit(1)
    """

    console.print("[bold green]{} has been installed with success[/]".format(nvim_name))
