import subprocess

from ..files import LocationDoesNotExist, NotADirectory
from ..resources import console, default_transient_progress


def configure(dir_path, args, app_name=""):
    """Invoke configure in the given directory

    Args:
        dir_path (Path): the directory in which invoke configure
        args (list): the arguments to pass to configure. It must be a list of string
            containing all arguments that must be passed to configure.

    Returns:
        int: the return code of configure. It it is different than zero then something
            went wrong.
        str: the standard output of configure.
        std: the standard error output of configure.

    Raises:
        LocationDoesNotExist: if the given directory does not exist.
        NotADirectory: if the given location is not a directory.
    """
    if app_name != "" and not app_name.startswith(" "):
        app_name = " {}".format(app_name)

    with default_transient_progress() as progress:
        progress.add_task("Configuring{}...".format(app_name), start=False)

        if not dir_path.exists():
            raise LocationDoesNotExist("{} does not exist".format(dir_path))

        if not dir_path.is_dir():
            raise NotADirectory("{} is not a directory".format(dir_path))

        args = ["./configure"] + args
        result = subprocess.run(args, cwd=dir_path, capture_output=True, text=True)

    if result.returncode == 0:
        console.print("Configuring{}...[bold green]Done![/]".format(app_name))

    return result.returncode, result.stdout, result.stderr


def Configure(dir_path, args, app_name=""):
    """Invoke Configure in the given directory

    Args:
        dir_path (Path): the directory in which invoke Configure
        args (list): the arguments to pass to Configure. It must be a list of string
            containing all arguments that must be passed to configure.

    Returns:
        int: the return code of Configure. It it is different than zero then something
            went wrong.
        str: the standard output of Configure.
        std: the standard error output of Configure.

    Raises:
        LocationDoesNotExist: if the given directory does not exist.
        NotADirectory: if the given location is not a directory.
    """
    if app_name != "" and not app_name.startswith(" "):
        app_name = " {}".format(app_name)

    with default_transient_progress() as progress:
        progress.add_task("Configuring{}...".format(app_name), start=False)

        if not dir_path.exists():
            raise LocationDoesNotExist("{} does not exist".format(dir_path))

        if not dir_path.is_dir():
            raise NotADirectory("{} is not a directory".format(dir_path))

        args = ["./Configure"] + args
        result = subprocess.run(args, cwd=dir_path, capture_output=True, text=True)

    if result.returncode == 0:
        console.print("Configuring{}...[bold green]Done![/]".format(app_name))

    return result.returncode, result.stdout, result.stderr
