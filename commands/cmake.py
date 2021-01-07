import click

from .utils.files import download_archive, extract_tarfile, move, remove
from .utils.make import bootstrap, make, make_install
from .utils.print import print_msg_titled, print_stdoutputs
from .utils.resources import console, local_path, packages_path, temp_path

cmake_name = "cmake"
cmake_version = "3.19.2"
cmake_homepage = "https://cmake.org/"
cmake_archive_link = (
    "https://github.com/Kitware/CMake/releases/download/v3.19.2/cmake-3.19.2.tar.gz"
)
cmake_archive_top_directory_name = "cmake-3.19.2"
cmake_archive_path = temp_path.joinpath("cmake.tar.gz")
cmake_package_path = packages_path.joinpath("cmake")
cmake_install_path = local_path


@click.group()
def cmake():
    """cmake commands group."""
    pass


@cmake.command()
def info():
    """print info on cmake."""
    print_msg_titled(
        "{} - {}".format(cmake_name, cmake_version),
        "home page: {}".format(cmake_homepage),
    )


@cmake.command()
def install():
    """install cmake locally."""
    # clone archive
    download_archive(cmake_archive_link, cmake_archive_path, cmake_name)

    # extract archive
    cmake_tmp_path = temp_path.joinpath(cmake_archive_top_directory_name)

    if cmake_tmp_path.exists():
        remove(cmake_tmp_path, "{}".format(cmake_tmp_path))

    extract_tarfile(cmake_archive_path, temp_path, cmake_name)

    # move temp directory to packages
    if cmake_package_path.exists():
        remove(cmake_package_path, "{}".format(cmake_package_path))

    move(cmake_tmp_path, cmake_package_path, cmake_name)

    # bootstrap
    returncode, stdout, stderr = bootstrap(
        cmake_package_path,
        [
            "--prefix={}".format(cmake_install_path),
            "--",
            "-DCMAKE_BUILD_TYPE:STRING=Release",
        ],
        cmake_name,
    )
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while bootsraping {}[/]".format(cmake_name), stdout, stderr
        )
        exit(1)

    # make
    returncode, stdout, stderr = make(cmake_package_path, [], cmake_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while making {}[/]".format(cmake_name), stdout, stderr
        )
        exit(1)

    # make install
    returncode, stdout, stderr = make_install(cmake_package_path, [], cmake_name)
    if returncode != 0:
        print_stdoutputs(
            "[bold red]Error while installing {}[/]".format(cmake_name), stdout, stderr
        )
        exit(1)

    console.print("[bold green]cmake has been installed with success[/]")
