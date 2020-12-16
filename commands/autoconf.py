import click

from .utils.resources import console, temp_path, packages_path, local_path
from .utils.files import download_archive, remove, extract_tarfile, move
from .utils.make import configure, make, make_install
from .utils.print import print_stdoutputs

autoconf_name = "autoconf"
autoconf_archive_link = "https://ftp.gnu.org/gnu/autoconf/autoconf-2.70.tar.gz"
autoconf_archive_top_directory_name = "autoconf-2.70"
autoconf_archive_path = temp_path.joinpath("autoconf.tar.gz")
autoconf_package_path = packages_path.joinpath("autoconf")
autoconf_install_path = local_path


@click.group()
def autoconf():
    """autoconf commands group."""
    pass


@autoconf.command()
def install():
    """install autoconf locally."""
    # clone archive
    download_archive(autoconf_archive_link, autoconf_archive_path, autoconf_name)

    # extract archive
    autoconf_tmp_path = temp_path.joinpath(autoconf_archive_top_directory_name)

    if autoconf_tmp_path.exists():
        remove(autoconf_tmp_path, "{}".format(autoconf_tmp_path))

    extract_tarfile(autoconf_archive_path, temp_path, autoconf_name)

    # move temp directory to repo
    if autoconf_package_path.exists():
        remove(autoconf_package_path, "{}".format(autoconf_package_path))

    move(autoconf_tmp_path, autoconf_package_path)

    # configure
    returncode, stdout, stderr = configure(autoconf_package_path, ["--prefix={}".format(autoconf_install_path)], autoconf_name)
    if returncode != 0:
        print_stdoutputs("[bold red]Error while configuring {}[/]".format(autoconf_name), stdout, stderr)
        exit(1)

    # make
    returncode, stdout, stderr = make(autoconf_package_path, [], autoconf_name)
    if returncode != 0:
        print_stdoutputs("[bold red]Error while making {}[/]".format(autoconf_name), stdout, stderr)
        exit(1)

    returncode, stdout, stderr = make_install(autoconf_package_path, [], autoconf_name)
    if returncode != 0:
        print_stdoutputs("[bold red]Error while installing {}[/]".format(autoconf_name), stdout, stderr)
        exit(1)

    console.print("[bold green]autoconf has been installed with success[/]")

