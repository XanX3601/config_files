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

nvim_repo_link = "https://github.com/neovim/neovim.git"
nvim_repo_path = repository_path.joinpath("neovim")
nvim_install_path = local_path.joinpath("neovim")
nvim_build_path = nvim_repo_path.joinpath("build")
nvim_bashrc_config_path = configs_path.joinpath("neovim/bash_nvim")
nvim_bashrc_line = "source {}/{}".format(
    bashrc_config_path, nvim_bashrc_config_path.name
)
nvim_init_path = configs_path.joinpath("neovim/init.vim")
nvim_config_path = config_path.joinpath("nvim")


@click.group()
def neovim():
    """neovim commmands group."""
    pass


@neovim.command()
def install():
    """install neovim locally."""
    # clone repository
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Cloning neovim repository...", start=False)

        if nvim_repo_path.exists():
            try:
                nvim_repo = git.Repo(nvim_repo_path)
            except:
                console.print(
                    "Error while cloning neovim repository",
                    justify="center",
                    style="bold red",
                )
                console.print("{} is not a git repository".format(nvim_repo_path))
                exit(1)
        else:
            nvim_repo = git.Repo.clone_from(nvim_repo_link, nvim_repo_path)

    console.print("Cloning neovim repository...[bold green]Done![/]")

    # update local repository
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Updating neovim repository", start=False)
        origin = nvim_repo.remotes.origin
        origin.pull()

    console.print("Updating neovim repository...[bold green]Done![/]")

    # make and install from local repository
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("Compiling and installing neovim", start=False)

        if nvim_build_path.exists():
            console.print("    Erasing previous build...")
            shutil.rmtree(nvim_build_path)

        args = ["make", "CMAKE_INSTALL_PREFIX={}".format(nvim_install_path)]
        console.print("    Compiling neovim...")
        result = subprocess.run(
            args, cwd=nvim_repo_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while compiling neovim", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

        args = ["make", "install"]
        console.print("    Installing neovim...")
        result = subprocess.run(
            args, cwd=nvim_repo_path, capture_output=True, text=True
        )

        if result.returncode != 0:
            console.print(
                "Error while installing neovim", justify="center", style="bold red"
            )
            console.rule("stdout")
            console.print(result.stdout)
            console.rule("stderr")
            console.print(result.stderr)
            exit(1)

    console.print("Compiling and installing neovim...[bold green]Done![/]")

    # install bash config
    console.print("Installing neovim bash config...", end="")

    shutil.copy(nvim_bashrc_config_path, bashrc_config_path)

    bash_nvim_line_found = False

    with open(bashrc_path, "r") as bashrc:
        for line in bashrc:
            line = line.strip()
            if line == nvim_bashrc_line:
                bash_nvim_line_found = True

    if not bash_nvim_line_found:
        with open(bashrc_path, "a") as bashrc:
            bashrc.write("\n# nvim config\n")
            bashrc.write("{}\n".format(nvim_bashrc_line))

    console.print("[bold green]Done[/]")

    # install nvim.init
    console.print("Installing neovim config file...", end="")

    if not config_path.exists():
        os.mkdir(nvim_config_path)

    if not nvim_config_path.exists():
        os.mkdir(nvim_config_path)

    shutil.copy(nvim_init_path, nvim_config_path)

    console.print("[bold green]Done[/]")
