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
    bashrc_config_path,
    bashrc_path,
    console,
    configs_path,
)

autoconf_archive_link = "https://ftp.gnu.org/gnu/autoconf/autoconf-2.70.tar.gz"
autoconf_archive_top_directory_name = "autoconf-2.70"
autoconf_archive_path = temp_path.joinpath("autoconf.tar.gz")
autoconf_package_path = package_path.joinpath("autoconf")
autoconf_install_path = local_path.joinpath("autoconf")
autoconf_bashrc_config_path = configs_path.joinpath("autoconf/bash_autoconf")
autoconf_bashrc_line = "source {}/{}".format(
    bashrc_config_path, autoconf_bashrc_config_path.name
)


@click.group()
def autoconf():
    """autoconf commands group."""
    pass


@autoconf.command()
def install():
    """install autoconf locally."""
    # clone archive
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        with open(autoconf_archive_path, "wb") as archive:
            task = progress.add_task("Downloading autoconf archive...", start=False)

            response = requests.get(
                autoconf_archive_link,
                stream=True,
                headers={"Accept-Encoding": ""},
            )
            total = int(response.headers.get("Content-Length"))

            progress.update(task_id=task, total=total)
            progress.start_task(task_id=task)

            for data in response.iter_content(chunk_size=1024):
                archive.write(data)
                progress.advance(task_id=task, advance=len(data))

    console.print("Downloading autoconf archive...[bold green]Done![/]")

    # extract archive
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Extracting autoconf archive...", start=False)

        autoconf_tmp_path = temp_path.joinpath(autoconf_archive_top_directory_name)
        if autoconf_tmp_path.exists():
            console.print("    Erasing {} directory...".format(autoconf_tmp_path))
            shutil.rmtree(autoconf_tmp_path)

        with tarfile.open(autoconf_archive_path) as archive:
            console.print("    Extracting archive...")
            archive.extractall(temp_path)

    console.print("Extracing autoconf archive...[bold green]Done![/]")

    # move temp directory to repo
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Moving archive content to package...", start=False)

        if autoconf_package_path.exists():
            console.print("    Erasing previous package...")
            shutil.rmtree(autoconf_package_path)

        console.print("    Moving archive content...")
        shutil.move(str(autoconf_tmp_path), str(autoconf_package_path))

    console.print("Moving archive content to package...[bold green]Done![/]")

    # configure
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Configuring autoconf...", start=False)

        args = ["./configure", "--prefix={}".format(autoconf_install_path)]
        result = subprocess.run(
            args, cwd=autoconf_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while configuring autoconf", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Configuring autoconf...[bold green]Done![/]")

    # make
    with Progress(
        "[progress.dexcription]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Compiling and installing autoconf...", start=False)

        args = ["make"]
        result = subprocess.run(
            args, cwd=autoconf_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while compiling autoconf", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

        # make install
        args = ["make", "install"]
        result = subprocess.run(
            args, cwd=autoconf_package_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while insalling autoconf", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Compiling and installing autoconf...[bold green]Done![/]")

    # install bashrc config
    console.print("Installing autoconf bash config...", end="")

    shutil.copy(autoconf_bashrc_config_path, bashrc_config_path)

    bash_line_found = False

    with open(bashrc_path, "r") as bashrc:
        for line in bashrc:
            line = line.strip()
            if line == autoconf_bashrc_line:
                bash_line_found = True

    if not bash_line_found:
        with open(bashrc_path, "a") as bashrc:
            bashrc.write("\n# autoconf config\n")
            bashrc.write("{}\n".format(autoconf_bashrc_line))

    console.print("[bold green]Done![/]")
