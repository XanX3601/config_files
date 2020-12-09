import click
import git
from .utils import repository_path, local_path
import subprocess

vifm_repo_path = repository_path.joinpath("vifm")
vifm_install_path = local_path.joinpath("vifm")


@click.group()
def vifm():
    """vifm commands group."""
    pass


@vifm.command()
def install():
    """install vifm locally."""
    # clone repository
    if vifm_repo_path.exists():
        try:
            vifm_repo = git.Repo(vifm_repo_path)
        except:
            exit(1)
    else:
        vifm_repo = git.Repo.clone_from(
            "https://github.com/vifm/vifm.git", vifm_repo_path
        )

    # update repository
    origin = vifm_repo.remotes.origin
    origin.pull()

    # configure
    args = ["./configure", "--prefix={}".format(vifm_install_path)]
    result = subprocess.run(args, cwd=vifm_repo_path, text=True)

    if result.returncode != 0:
        print(result.stderr)

    # make
    args = ["make"]
    result = subprocess.run(args, cwd=vifm_repo_path, text=True)

    if result.returncode != 0:
        print(result.stderr)

    # install
    args = ["make", "install"]
    result = subprocess.run(args, cwd=vifm_repo_path, text=True)

    if result.returncode != 0:
        print(result.stderr)
