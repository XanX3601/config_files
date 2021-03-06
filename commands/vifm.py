import click

from .utils.files import LocationExists, copy, create_directory
from .utils.git import (
    NotAGitRepo,
    clone_repository,
    remove_local_changes,
    update_repository,
)
from .utils.make import autoreconf, configure, make, make_install
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.resources import (
    config_path,
    configs_path,
    console,
    local_path,
    repositories_path,
)
from .ncurses import install as ncurses_install

vifm_name = "vifm"
vifm_homepage = "https://vifm.info/"
vifm_repo_link = "https://github.com/vifm/vifm.git"
vifm_repo_path = repositories_path.joinpath("vifm")
vifm_install_path = local_path
vifm_vimfrc_path = configs_path.joinpath("vifm/vifmrc")
vifm_config_path = config_path.joinpath("vifm")


@click.group()
def vifm():
    """vifm commmands group."""
    pass


@vifm.command()
def info():
    """print info on vifm."""
    print_msg_titled(
        "{}".format(vifm_name),
        "home page: {}".format(vifm_homepage),
    )


@vifm.command()
@click.option("--with-dependencies", is_flag=True, help="Install with dependencies")
@click.pass_context
def install(ctx, with_dependencies):
    """install vifm locally."""
    # handle dependencies
    if with_dependencies:
        ctx.invoke(ncurses_install)

    # clone repository
    try:
        clone_repository(vifm_repo_link, vifm_repo_path, vifm_name)
    except LocationExists as exception:
        pass

    # remove local changes
    try:
        remove_local_changes(vifm_repo_path, vifm_name)
    except NotAGitRepo as exception:
        print_msg_titled(
            "Error while updating {} repository".format(vifm_name), str(exception)
        )

    # update local repository
    try:
        update_repository(vifm_repo_path, vifm_name)
    except NotAGitRepo as exception:
        print_msg_titled(
            "Error while updating {} repository".format(vifm_name), str(exception)
        )

    # autoreconf
    returncode, stdout, stderr = autoreconf(vifm_repo_path, ["-f", "-i"], vifm_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while reconfiguring {}[/]".format(vifm_name),
            stdout,
            stderr,
        )
        exit(1)

    # configure
    returncode, stdout, stderr = configure(
        vifm_repo_path,
        [
            "--prefix={}".format(vifm_install_path),
            "--with-curses={}".format(local_path),
        ],
        vifm_name,
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while configuring {}[/]".format(vifm_name), stdout, stderr
        )
        exit(1)

    # make
    returncode, stdout, stderr = make(
        vifm_repo_path, ["CMAKE_INSTALL_PREFIX={}".format(vifm_install_path)], vifm_name
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while compiling {}[/]".format(vifm_name), stdout, stderr
        )
        exit(1)

    # make install
    returncode, stdout, stderr = make_install(vifm_repo_path, [], vifm_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while installing {}[/]".format(vifm_name), stdout, stderr
        )
        exit(1)

    # install vifm.init
    if not vifm_config_path.exists():
        create_directory(vifm_config_path)

    copy(
        vifm_vimfrc_path, vifm_config_path, "{} {}".format(vifm_name, vifm_vimfrc_path)
    )

    console.print("[bold green]{} has been installed with success[/]".format(vifm_name))
