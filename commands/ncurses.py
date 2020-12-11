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
    configs_path,
)

ncurses_archive_link = "https://invisible-island.net/datafiles/release/ncurses.tar.gz"
ncurses_archive_top_directory_name = "ncurses-6.2"
ncurses_archive_path = temp_path.joinpath("ncurses.tar.gz")
ncurses_package_path = package_path.joinpath("ncurses")
ncurses_install_path = local_path.joinpath("ncurses")
ncurses_bashrc_config_path = configs_path.joinpath("ncurses/bash_ncurses")
ncurses_bashrc_line = "source {}/{}".format(
    bashrc_config_path, ncurses_bashrc_config_path.name
)


@click.group()
def ncurses():
    """ncurses commands group."""
    pass


@ncurses.command()
def install():
    """install ncurses locally."""
    # clone archive
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task("Downloading ncurses archive...", start=False)

        with open(ncurses_archive_path, "wb") as archive:
            response = requests.get(
                ncurses_archive_link,
                stream=True,
                headers={"Accept-Encoding": ""},
            )
            total = int(response.headers.get("Content-Length"))

            progress.update(task_id=task, total=total)
            progress.start_task(task_id=task)

            for data in response.iter_content(chunk_size=1024):
                archive.write(data)
                progress.advance(task_id=task, advance=len(data))

    console.print("Downloading ncurses archive...[bold green]Done![/]")

    # extract archive
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Extracting ncurses archive...", start=False)

        ncurses_tmp_path = temp_path.joinpath(ncurses_archive_top_directory_name)
        if ncurses_tmp_path.exists():
            console.print("    Erasing {} directory...".format(ncurses_tmp_path))
            shutil.rmtree(ncurses_tmp_path)

        with tarfile.open(ncurses_archive_path) as archive:
            console.print("    Extracting archive...")
            archive.extractall(temp_path)

    console.print("Extracing ncurses archive...[bold green]Done![/]")

    # move temp directory to package
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Moving archive content to package...", start=False)

        if ncurses_package_path.exists():
            console.print("    Erasing previous package...")
            shutil.rmtree(ncurses_package_path)

        console.print("    Moving archive content...")
        shutil.move(str(ncurses_tmp_path), str(ncurses_package_path))

    console.print("Moving archive content to package...[bold green]Done![/]")

    # configure
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Configuring ncurses...", start=False)

        args = ["./configure", "--prefix={}".format(ncurses_install_path)]
        result = subprocess.run(
            args, cwd=ncurses_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while configuring ncurses", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Configuring ncurses...[bold green]Done![/]")

    # make
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Compiling and installing ncurses...", start=False)

        args = ["make"]
        result = subprocess.run(
            args, cwd=ncurses_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while compiling ncurses", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

        # make install
        args = ["make", "install"]
        result = subprocess.run(
            args, cwd=ncurses_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while insalling ncurses", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Compiling and installing ncurses...[bold green]Done![/]")

    # configure
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Configuring ncursesw...", start=False)

        args = [
            "./configure",
            "--prefix={}".format(ncurses_install_path),
            "--enable-widec",
        ]
        result = subprocess.run(
            args, cwd=ncurses_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while configuring ncurses", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Configuring ncursesw...[bold green]Done![/]")

    # make
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Compiling and installing ncursesw...", start=False)

        args = ["make"]
        result = subprocess.run(
            args, cwd=ncurses_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while compiling ncursesw", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

        # make install
        args = ["make", "install"]
        result = subprocess.run(
            args, cwd=ncurses_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while insalling ncursesw", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Compiling and installing ncursesw...[bold green]Done![/]")

    # install bashrc config
    console.print("Installing ncurses bash config...", end="")

    shutil.copy(ncurses_bashrc_config_path, bashrc_config_path)

    bash_line_found = False

    with open(bashrc_path, "r") as bashrc:
        for line in bashrc:
            line = line.strip()
            if line == ncurses_bashrc_line:
                bash_line_found = True

    if not bash_line_found:
        with open(bashrc_path, "a") as bashrc:
            bashrc.write("\n# ncurses config\n")
            bashrc.write("{}\n".format(ncurses_bashrc_line))

    console.print("[bold green]Done![/]")
