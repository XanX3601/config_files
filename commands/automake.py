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

automake_archive_link = "https://ftp.gnu.org/gnu/automake/automake-1.16.3.tar.gz"
automake_archive_top_directory_name = "automake-1.16.3"
automake_archive_path = temp_path.joinpath("automake.tar.gz")
automake_package_path = package_path.joinpath("automake")
automake_install_path = local_path.joinpath("automake")
automake_bashrc_config_path = current_path.joinpath("automake/bash_automake")
automake_bashrc_line = "source {}/{}".format(
    bashrc_config_path, automake_bashrc_config_path.name
)


@click.group()
def automake():
    """automake commands group."""
    pass


@automake.command()
def install():
    """install libtool locally."""
    # clone archive
    with open(automake_archive_path, "wb") as archive:
        response = requests.get(automake_archive_link, stream=True)

        for data in response.iter_content(chunk_size=1024):
            archive.write(data)

    # extract archive
    automake_tmp_path = temp_path.joinpath(automake_archive_top_directory_name)
    if automake_tmp_path.exists():
        shutil.rmtree(automake_tmp_path)

    with tarfile.open(automake_archive_path) as archive:
        archive.extractall(temp_path)

    # move temp directory to repo
    if automake_package_path.exists():
        shutil.rmtree(automake_package_path)

    shutil.move(str(automake_tmp_path), str(automake_package_path))

    # configure
    args = ["./configure", "--prefix={}".format(automake_install_path)]
    result = subprocess.run(
        args, cwd=automake_package_path, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(result.stderr)

    # make
    args = ["make"]
    result = subprocess.run(
        args, cwd=automake_package_path, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(result.stderr)

    # make install
    args = ["make", "install"]
    result = subprocess.run(
        args, cwd=automake_package_path, capture_output=True, text=True
    )

    if result.returncode != 0:
        print(result.stderr)

    # install bashrc config
    shutil.copy(automake_bashrc_config_path, bashrc_config_path)

    bash_line_found = False

    with open(bashrc_path, "r") as bashrc:
        for line in bashrc:
            line = line.strip()
            if line == automake_bashrc_line:
                bash_line_found = True

    if not bash_line_found:
        with open(bashrc_path, "a") as bashrc:
            bashrc.write("\n# automake config\n")
            bashrc.write("{}\n".format(automake_bashrc_line))
