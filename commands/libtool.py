import click
import requests
import tarfile
import subprocess
import shutil

from .utils import (
    temp_path,
    package_path,
    local_path,
    current_path,
    bashrc_config_path,
    bashrc_path,
)

libtool_archive_link = "https://ftpmirror.gnu.org/libtool/libtool-2.4.6.tar.gz"
libtool_archive_top_directory_name = "libtool-2.4.6"
libtool_archive_path = temp_path.joinpath("libtool.tar.gz")
libtool_package_path = package_path.joinpath("libtool")
libtool_install_path = local_path.joinpath("libtool")
libtool_bashrc_config_path = current_path.joinpath("libtool/bash_libtool")
libtool_bashrc_line = "source {}/{}".format(
    bashrc_config_path, libtool_bashrc_config_path.name
)


@click.group()
def libtool():
    """libtool commands group."""
    pass


@libtool.command()
def install():
    """install libtool locally."""
    # clone archive
    with open(libtool_archive_path, "wb") as archive:
        response = requests.get(libtool_archive_link, stream=True)

        for data in response.iter_content(chunk_size=1024):
            archive.write(data)

    print(1)

    # extract archive
    libtool_tmp_path = temp_path.joinpath(libtool_archive_top_directory_name)
    if libtool_tmp_path.exists():
        shutil.rmtree(libtool_tmp_path)

    with tarfile.open(libtool_archive_path) as archive:
        archive.extractall(temp_path)

    # move temp directory to repo
    if libtool_package_path.exists():
        shutil.rmtree(libtool_package_path)

    shutil.move(str(libtool_tmp_path), str(libtool_package_path))

    print(1)

    # configure
    args = ["./configure", "--prefix={}".format(libtool_install_path)]
    result = subprocess.run(
        args, cwd=libtool_package_path, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(result.stderr)

    print(1)

    # make
    args = ["make"]
    result = subprocess.run(
        args, cwd=libtool_package_path, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(result.stderr)

    print(1)

    # make install
    args = ["make", "install"]
    result = subprocess.run(
        args, cwd=libtool_package_path, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(result.stderr)

    print(1)

    # install bashrc config
    shutil.copy(libtool_bashrc_config_path, bashrc_config_path)

    bash_line_found = False

    with open(bashrc_path, "r") as bashrc:
        for line in bashrc:
            line = line.strip()
            if line == libtool_bashrc_line:
                bash_line_found = True

    if not bash_line_found:
        with open(bashrc_path, "a") as bashrc:
            bashrc.write("\n# libtool config\n")
            bashrc.write("{}\n".format(libtool_bashrc_line))
