import click

from .utils.files import download_archive, extract_tarfile, move, remove
from .utils.make import configure, make, make_install
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.resources import console, local_path, packages_path, temp_path

node_name = "node"
node_version = "14.15.3"
node_homepage = "https://nodejs.org/en/"
node_archive_link = "https://nodejs.org/dist/v14.15.3/node-v14.15.3-linux-x64.tar.xz"
node_archive_top_directory_name = "node-v14.15.3-linux-x64"
node_archive_path = temp_path.joinpath("node.tar.xz")
node_install_path = local_path


@click.group()
def node():
    """node commands group."""
    pass


@node.command()
def info():
    """print info on node."""
    print_msg_titled(
        "{} - {}".format(node_name, node_version),
        "home page: {}".format(node_homepage),
    )


@node.command()
def install():
    """install node locally."""
    # clone archive
    download_archive(node_archive_link, node_archive_path, node_name)

    # extract archive
    node_tmp_path = temp_path.joinpath(node_archive_top_directory_name)

    if node_tmp_path.exists():
        remove(node_tmp_path, "{}".format(node_tmp_path))

    extract_tarfile(node_archive_path, temp_path, node_name)

    # move temp directory to install path
    move(node_tmp_path, node_install_path, node_name, True)

    console.print("[bold green]{} has been installed with success[/]".format(node_name))
