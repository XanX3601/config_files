import click

from .utils.resources import console, temp_path, packages_path, local_path
from .utils.files import download_archive, remove, extract_tarfile, move
from .utils.make import configure, make, make_install
from .utils.print import print_stdoutputs

automake_name = "automake"
automake_archive_link = "https://ftp.gnu.org/gnu/automake/automake-1.16.3.tar.gz"
automake_archive_top_directory_name = "automake-1.16.3"
automake_archive_path = temp_path.joinpath("automake.tar.gz")
automake_package_path = packages_path.joinpath("automake")
automake_install_path = local_path


@click.group()
def automake():
    """automake commands group."""
    pass


@automake.command()
def install():
    """install automake locally."""
    # clone archive
    download_archive(automake_archive_link, automake_archive_path, automake_name)

    # extract archive
    automake_tmp_path = temp_path.joinpath(automake_archive_top_directory_name)

    if automake_tmp_path.exists():
        remove(automake_tmp_path, "{}".format(automake_tmp_path))

    extract_tarfile(automake_archive_path, temp_path, automake_name)

    # move temp directory to repo
    if automake_package_path.exists():
        remove(automake_package_path, "{}".format(automake_package_path))

    move(automake_tmp_path, automake_package_path)

    # configure
    returncode, stdout, stderr = configure(automake_package_path, ["--prefix={}".format(automake_install_path)], automake_name)
    if returncode != 0:
        print_stdoutputs("[bold red]Error while configuring {}[/]".format(automake_name), stdout, stderr)
        exit(1)

    # make
    returncode, stdout, stderr = make(automake_package_path, [], automake_name)
    if returncode != 0:
        print_stdoutputs("[bold red]Error while making {}[/]".format(automake_name), stdout, stderr)
        exit(1)

    returncode, stdout, stderr = make_install(automake_package_path, [], automake_name)
    if returncode != 0:
        print_stdoutputs("[bold red]Error while installing {}[/]".format(automake_name), stdout, stderr)
        exit(1)

    console.print("[bold green]automake has been installed with success[/]")

