import click

from .utils.files import download_archive, extract_tarfile, move, remove
from .utils.make import configure, make, make_install
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.resources import console, local_path, packages_path, temp_path

libtool_name = "libtool"
libtool_version = "2.4.6"
libtool_homepage = "https://www.gnu.org/software/libtool/"
libtool_archive_link = "https://ftpmirror.gnu.org/libtool/libtool-2.4.6.tar.gz"
libtool_archive_top_directory_name = "libtool-2.4.6"
libtool_archive_path = temp_path.joinpath("libtool.tar.gz")
libtool_package_path = packages_path.joinpath("libtool")
libtool_install_path = local_path


@click.group()
def libtool():
    """libtool commands group."""
    pass


@libtool.command()
def info():
    """print info on libtool."""
    print_msg_titled(
        "{} - {}".format(libtool_name, libtool_version),
        "home page: {}".format(libtool_homepage),
    )


@libtool.command()
def install():
    """install libtool locally."""
    # clone archive
    download_archive(libtool_archive_link, libtool_archive_path, libtool_name)

    # extract archive
    libtool_tmp_path = temp_path.joinpath(libtool_archive_top_directory_name)

    if libtool_tmp_path.exists():
        remove(libtool_tmp_path, "{}".format(libtool_tmp_path))

    extract_tarfile(libtool_archive_path, temp_path, libtool_name)

    # move temp directory to repo
    if libtool_package_path.exists():
        remove(libtool_package_path, "{}".format(libtool_package_path))

    move(libtool_tmp_path, libtool_package_path, libtool_name)

    # configure
    returncode, stdout, stderr = configure(
        libtool_package_path, ["--prefix={}".format(libtool_install_path)], libtool_name
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while configuring {}[/]".format(libtool_name),
            stdout,
            stderr,
        )
        exit(1)

    # make
    returncode, stdout, stderr = make(libtool_package_path, [], libtool_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while making {}[/]".format(libtool_name), stdout, stderr
        )
        exit(1)

    returncode, stdout, stderr = make_install(libtool_package_path, [], libtool_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while installing {}[/]".format(libtool_name),
            stdout,
            stderr,
        )
        exit(1)

    console.print("[bold green]libtool has been installed with success[/]")
