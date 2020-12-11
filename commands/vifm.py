import os
import shutil
import subprocess

import click
import git
from rich.progress import BarColumn, Progress

from .utils import (
    bashrc_config_path,
    bashrc_path,
    config_path,
    console,
    local_path,
    repository_path,
    configs_path,
)

vifm_repo_link = "https://github.com/vifm/vifm.git"
vifm_repo_path = repository_path.joinpath("vifm")
vifm_install_path = local_path.joinpath("vifm")
vifm_bashrc_config_path = configs_path.joinpath("vifm/bash_vifm")
vifm_bashrc_line = "source {}/{}".format(
    bashrc_config_path, vifm_bashrc_config_path.name
)
vifm_vimfrc_path = configs_path.joinpath("vifm/vifmrc")
vifm_config_path = config_path.joinpath("vifm")


@click.group()
def vifm():
    """vifm commmands group."""
    pass


@vifm.command()
def install():
    """install vifm locally."""
    # clone repository
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Cloning vifm repository...", start=False)

        if vifm_repo_path.exists():
            try:
                vifm_repo = git.Repo(vifm_repo_path)
            except:
                console.print(
                    "Error while cloning vifm repository",
                    justify="center",
                    style="bold red",
                )
                console.print("{} is not a git repository".format(vifm_repo_path))
                exit(1)
        else:
            vifm_repo = git.Repo.clone_from(vifm_repo_link, vifm_repo_path)

    console.print("Cloning vifm repository...[bold green]Done![/]")

    # update local repository
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Updating vifm repository", start=False)
        origin = vifm_repo.remotes.origin
        origin.pull()

    console.print("Updating vifm repository...[bold green]Done![/]")

    # autoreconf
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Autoreconf vifm...", start=False)

        args = ["autoreconf", "-f", "-i"]
        result = subprocess.run(
            args, cwd=vifm_repo_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while autoreconf vifm", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Autoreconf vifm...[bold green]Done![/]")

    # configure
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Configuring vifm...", start=False)

        args = ["./configure", "--prefix={}".format(vifm_install_path)]
        result = subprocess.run(
            args, cwd=vifm_repo_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while configurin vifm", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Configuring vifm...[bold green]Done![/]")

    # make and install from local repository
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Compiling and installing vifm", start=False)

        args = ["make"]
        console.print("    Compiling vifm...")
        result = subprocess.run(
            args, cwd=vifm_repo_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while compiling vifm", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

        args = ["make", "install"]
        console.print("    Installing vifm...")
        result = subprocess.run(
            args, cwd=vifm_repo_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while installing vifm", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Compiling and installing vifm...[bold green]Done![/]")

    # install bash config
    console.print("Installing vifm bash config...", end="")

    shutil.copy(vifm_bashrc_config_path, bashrc_config_path)

    bashrc_line_found = False

    with open(bashrc_path, "r") as bashrc:
        for line in bashrc:
            line = line.strip()
            if line == vifm_bashrc_line:
                bashrc_line_found = True

    if not bashrc_line_found:
        with open(bashrc_path, "a") as bashrc:
            bashrc.write("\n# vifm config\n")
            bashrc.write("{}\n".format(vifm_bashrc_line))

    console.print("[bold green]Done[/]")

    # install nvim.init
    console.print("Installing vifm config file...", end="")

    if not vifm_config_path.exists():
        os.mkdir(vifm_config_path)

    shutil.copy(vifm_vimfrc_path, vifm_config_path)

    console.print("[bold green]Done[/]")
