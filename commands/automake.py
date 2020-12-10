import click
import requests
import tarfile
import subprocess
from rich.progress import Progress, BarColumn, DownloadColumn
import shutil

from .utils import (
    temp_path,
    package_path,
    local_path,
    current_path,
    bashrc_config_path,
    bashrc_path,
    console,
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
    """install automake locally."""
    # clone archive
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        with open(automake_archive_path, "wb") as archive:
            task = progress.add_task("Downloading automake archive...", start=False)

            response = requests.get(
                automake_archive_link,
                stream=True,
                headers={"Accept-Encoding": ""},
            )
            total = int(response.headers.get("Content-Length"))

            progress.update(task_id=task, total=total)
            progress.start_task(task_id=task)

            for data in response.iter_content(chunk_size=1024):
                archive.write(data)
                progress.advance(task_id=task, advance=len(data))

    console.print("Downloading automake archive...[bold green]Done![/]")

    # extract archive
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Extracting automake archive...", start=False)

        automake_tmp_path = temp_path.joinpath(automake_archive_top_directory_name)
        if automake_tmp_path.exists():
            console.print("    Erasing {} directory...".format(automake_tmp_path))
            shutil.rmtree(automake_tmp_path)

        with tarfile.open(automake_archive_path) as archive:
            console.print("    Extracting archive...")
            archive.extractall(temp_path)

    console.print("Extracing automake archive...[bold green]Done![/]")

    # move temp directory to repo
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Moving archive content to package...", start=False)

        if automake_package_path.exists():
            console.print("    Erasing previous package...")
            shutil.rmtree(automake_package_path)

        console.print("    Moving archive content...")
        shutil.move(str(automake_tmp_path), str(automake_package_path))

    console.print("Moving archive content to package...[bold green]Done![/]")

    # configure
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Configuring automake...", start=False)

        args = ["./configure", "--prefix={}".format(automake_install_path)]
        result = subprocess.run(
            args, cwd=automake_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while configuring automake", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Configuring automake...[bold green]Done![/]")

    # make
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Compiling and installing automake...", start=False)

        args = ["make"]
        result = subprocess.run(
            args, cwd=automake_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while compiling automake", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

        # make install
        args = ["make", "install"]
        result = subprocess.run(
            args, cwd=automake_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while insalling automake", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Compiling and installing automake...[bold green]Done![/]")

    # install bashrc config
    console.print("Installing automake bash config...", end="")

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

    console.print("[bold green]Done![/]")
