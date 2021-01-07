import click

from .utils.files import download_archive, extract_tarfile, move, remove
from .utils.make import configure, make, make_install
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.resources import console, local_path, packages_path, temp_path

ncurses_name = "ncurses"
ncurses_version = "6.2"
ncurses_homepage = "https://invisible-island.net/ncurses/"
ncurses_archive_link = "https://invisible-island.net/datafiles/release/ncurses.tar.gz"
ncurses_archive_top_directory_name = "ncurses-6.2"
ncurses_archive_path = temp_path.joinpath("ncurses.tar.gz")
ncurses_package_path = packages_path.joinpath("ncurses")
ncurses_install_path = local_path


@click.group()
def ncurses():
    """ncurses commands group."""
    pass


@ncurses.command()
def info():
    """print info on ncurses."""
    print_msg_titled(
        "{} - {}".format(ncurses_name, ncurses_version),
        "home page: {}".format(ncurses_homepage),
    )


@ncurses.command()
def install():
    """install ncurses locally."""
    # clone archive
    download_archive(ncurses_archive_link, ncurses_archive_path, ncurses_name)

    # extract archive
    ncurses_tmp_path = temp_path.joinpath(ncurses_archive_top_directory_name)

    if ncurses_tmp_path.exists():
        remove(ncurses_tmp_path, "{}".format(ncurses_tmp_path))

    extract_tarfile(ncurses_archive_path, temp_path, ncurses_name)

    # move temp directory to repo
    if ncurses_package_path.exists():
        remove(ncurses_package_path, "{}".format(ncurses_package_path))

    move(ncurses_tmp_path, ncurses_package_path, ncurses_name)

    # configure
    returncode, stdout, stderr = configure(
        ncurses_package_path,
        ["--prefix={}".format(ncurses_install_path), "--with-shared"],
        ncurses_name,
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while configuring {}[/]".format(ncurses_name),
            stdout,
            stderr,
        )
        exit(1)

    # make
    returncode, stdout, stderr = make(ncurses_package_path, [], ncurses_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while making {}[/]".format(ncurses_name), stdout, stderr
        )
        exit(1)

    returncode, stdout, stderr = make_install(ncurses_package_path, [], ncurses_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while installing {}[/]".format(ncurses_name),
            stdout,
            stderr,
        )
        exit(1)

    ncursesw_name = "{}w".format(ncurses_name)

    # configure
    returncode, stdout, stderr = configure(
        ncurses_package_path,
        ["--prefix={}".format(ncurses_install_path), "--enable-widec", "--with-shared"],
        ncursesw_name,
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while configuring {}[/]".format(ncursesw_name),
            stdout,
            stderr,
        )
        exit(1)

    # make
    returncode, stdout, stderr = make(ncurses_package_path, [], ncursesw_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while making {}[/]".format(ncursesw_name), stdout, stderr
        )
        exit(1)

    returncode, stdout, stderr = make_install(ncurses_package_path, [], ncursesw_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while installing {}[/]".format(ncursesw_name),
            stdout,
            stderr,
        )
        exit(1)

    console.print("[bold green]ncurses has been installed with success[/]")
