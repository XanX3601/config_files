"""Wrapper for git actions."""

import git

from ..files import LocationDoesNotExist, LocationExists
from ..resources import console, default_transient_progress
from .CloneProgress import CloneProgress
from .NotAGitRepo import NotAGitRepo


def clone_repository(repo_link, repo_path, repo_name=""):
    """Clone a repository in the repository directory.

    Clone the given repository in the given location. If the given location
    already exists, an error is raised.

    Args:
        repo_link (str): link to repository origin
        repo_path (Path): the location to where clone the repo
        app_name (str): name of the repository used in print. Default to empty

    Raises:
        LocationExists: if ``repo_path`` already exists.
    """

    if repo_name != "" and not repo_name.endswith(" "):
        repo_name = "{} ".format(repo_name)

    with default_transient_progress() as progress:
        task_id = progress.add_task(
            "Cloning {}repository...".format(repo_name), start=False
        )

        if repo_path.exists():
            raise LocationExists("{} already exists".format(repo_path))

        git.Repo.clone_from(
            repo_link, repo_path, progress=CloneProgress(progress, task_id)
        )

    console.print("Cloning {}repository...[bold green]Done![/]".format(repo_name))


def update_repository(repo_path, repo_name=""):
    """Update the given repository.

    Execute a ``git pull`` on the given repo. If the repository can not be opened
    an error is raised. If the repository does not exist, an error is also raised.

    Args:
        repo_path (Path): the path to the repository to update

    Raises:
        LocationDoesNotExist: when the repository does not exist
        NotAGitRepo: when the repository can not be opened
    """
    if repo_name != "" and not repo_name.endswith(" "):
        repo_name = "{} ".format(repo_name)

    with default_transient_progress() as progress:
        progress.add_task("Updating {}repository...".format(repo_name, start=False))

        if not repo_path.exists():
            raise LocationDoesNotExist("{} does not exist".format(repo_path))

        try:
            repo = git.Repo(repo_path)
        except:
            raise NotAGitRepo("{} is not a git repository".format(repo_path))

        origin = repo.remotes.origin
        origin.pull()

    console.print("Updating {}repository...[bold green]Done![/]".format(repo_name))


def remove_local_changes(repo_path, repo_name=""):
    """Remove all local changes in a repository.

    Args:
        repo_path (Path): the path to the repository to clean.
        repo_name (str): the name of the repository, used in printed messages only.

    Raises:
        LocationDoesNotExist: when the repository does not exists
        NotAGitRepo: when the repository can not be opened
    """
    if repo_name != "" and not repo_name.endswith(" "):
        repo_name = "{} ".format(repo_name)

    with default_transient_progress() as progress:
        progress.add_task("Removing {}local changes...".format(repo_name), start=False)

        if not repo_path.exists():
            raise LocationDoesNotExist("{} does not exist".format(repo_path))

        try:
            repo = git.Repo(repo_path)
        except:
            raise NotAGitRepo("{} is not a git repository".format(repo_path))

        repo.git.reset("--hard")

    console.print("Removing {}local changes...[bold green]Done![/]".format(repo_name))
