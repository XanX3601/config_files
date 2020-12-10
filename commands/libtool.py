import click
import requests
import tarfile
import subprocess
import shutil
from rich.progress import Progress, BarColumn, DownloadColumn

from .utils import (
    temp_path,
    package_path,
    local_path,
    current_path,
    bashrc_config_path,
    bashrc_path,
    console,
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
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Downloading libtool archive...", start=False)

        with open(libtool_archive_path, "wb") as archive:
            response = requests.get(
                libtool_archive_link,
                stream=True,
                headers={"Accept-Encoding": ""},
            )
            total = int(response.headers.get("Content-Length"))

            progress.update(task_id=task, total=total)
            progress.start_task(task_id=task)

            for data in response.iter_content(chunk_size=1024):
                archive.write(data)
                progress.advance(task_id=task, advance=len(data))

    console.print("Downloading libtool archive...[bold green]Done![/]")

    # extract archive
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Extracting libtool archive...", start=False)

        libtool_tmp_path = temp_path.joinpath(libtool_archive_top_directory_name)
        if libtool_tmp_path.exists():
            console.print("    Erasing {} directory...".format(libtool_tmp_path))
            shutil.rmtree(libtool_tmp_path)

        with tarfile.open(libtool_archive_path) as archive:
            console.print("    Extracting archive...")
            archive.extractall(temp_path)

    console.print("Extracing libtool archive...[bold green]Done![/]")

    # move temp directory to package
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Moving archive content to package...", start=False)

        if libtool_package_path.exists():
            console.print("    Erasing previous package...")
            shutil.rmtree(libtool_package_path)

        console.print("    Moving archive content...")
        shutil.move(str(libtool_tmp_path), str(libtool_package_path))

    console.print("Moving archive content to package...[bold green]Done![/]")

    # configure
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Configuring libtool...", start=False)

        args = ["./configure", "--prefix={}".format(libtool_install_path)]
        result = subprocess.run(
            args, cwd=libtool_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while configuring libtool", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Configuring libtool...[bold green]Done![/]")

    # make
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Compiling and installing libtool...", start=False)

        args = ["make"]
        result = subprocess.run(
            args, cwd=libtool_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while compiling libtool", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

        # make install
        args = ["make", "install"]
        result = subprocess.run(
            args, cwd=libtool_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while insalling libtool", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Compiling and installing libtool...[bold green]Done![/]")

    # install bashrc config
    console.print("Installing libtool bash config...", end="")

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

    console.print("[bold green]Done![/]")
