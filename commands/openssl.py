import click

from .utils.files import LocationExists, copy, create_directory
from .utils.git import (NotAGitRepo, clone_repository, remove_local_changes,
                        update_repository)
from .utils.make import Configure, make, make_install
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.resources import (config_path, configs_path, console, home_path,
                              local_path, repositories_path)

openssl_name = "openssl"
openssl_homepage = "https://www.openssl.org/"
openssl_repo_link = "https://github.com/openssl/openssl.git"
openssl_repo_path = repositories_path.joinpath("openssl")
openssl_install_path = local_path
openssl_directory = home_path.joinpath(".ssl")
openssl_vimfrc_path = configs_path.joinpath("openssl/opensslrc")
openssl_config_path = config_path.joinpath("openssl")


@click.group()
def openssl():
    """openssl commmands group."""
    pass


@openssl.command()
def info():
    """print info on openssl."""
    print_msg_titled(
        "{}".format(openssl_name),
        "home page: {}".format(openssl_homepage),
    )


@openssl.command()
def install():
    """install openssl locally."""
    # clone repository
    try:
        clone_repository(openssl_repo_link, openssl_repo_path, openssl_name)
    except LocationExists as exception:
        pass

    # remove local changes
    try:
        remove_local_changes(openssl_repo_path, openssl_name)
    except NotAGitRepo as exception:
        print_msg_titled(
            "Error while updating {} repository".format(openssl_name), str(exception)
        )

    # update local repository
    try:
        update_repository(openssl_repo_path, openssl_name)
    except NotAGitRepo as exception:
        print_msg_titled(
            "Error while updating {} repository".format(openssl_name), str(exception)
        )

    # Configure
    returncode, stdout, stderr = Configure(
        openssl_repo_path,
        [
            "--prefix={}".format(openssl_install_path),
            "--openssldir={}".format(openssl_directory),
        ],
        openssl_name,
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while Configuring {}[/]".format(openssl_name),
            stdout,
            stderr,
        )

    # make
    returncode, stdout, stderr = make(openssl_repo_path, [], openssl_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while compiling {}[/]".format(openssl_name), stdout, stderr
        )

    # make install
    returncode, stdout, stderr = make_install(openssl_repo_path, [], openssl_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while installing {}[/]".format(openssl_name),
            stdout,
            stderr,
        )

    console.print(
        "[bold green]{} has been installed with success[/]".format(openssl_name)
    )
