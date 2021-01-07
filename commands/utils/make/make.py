import subprocess

from ..files import LocationDoesNotExist, NotADirectory
from ..resources import console, default_transient_progress


def make(dir_path, args, app_name=""):
    """Invoke make in the given directory.

    Args:
        dir_path (Path): the directory in which invoke make.
        args (list): the arguments to pass to make. It must be a list of string
            containing all arguments that must be passed to make.

    Returns:
        int: the return code of make. If it is different than zero then something
            went wrong.
        str: the standard output of make
        std: the standard error output of make

    Raises:
        LocationDoesNotExist: if the given directory does not exist.
        NotADirectory: if the given location is not a directory.
    """
    if app_name != "" and not app_name.startswith(" "):
        app_name = " {}".format(app_name)

    with default_transient_progress() as progress:
        progress.add_task("Making{}...".format(app_name), start=False)

        if not dir_path.exists():
            raise LocationDoesNotExist("{} does not exist".format(dir_path))

        if not dir_path.is_dir():
            raise NotADirectory("{} is not a directory".format(dir_path))

        args = ["make"] + args
        result = subprocess.run(args, cwd=dir_path, capture_output=True, text=True)

    if result.returncode == 0:
        console.print("Making{}...[bold green]Done![/]".format(app_name))

    return result.returncode, result.stdout, result.stderr


def make_install(dir_path, args, app_name=""):
    """Invoke make install in the given directory.

    Args:
        dir_path (Path): the directory in which invoke make install.
        args (list): the arguments to pass to make. It must be a list of string
            containing all arguments that must be passed to make install.

    Returns:
        int: the return code of make install. If it is different than zero then something
            went wrong.
        str: the standard output of make install
        std: the standard error output of make install

    Raises:
        LocationDoesNotExist: if the given directory does not exist.
        NotADirectory: if the given location is not a directory.
    """
    if app_name != "" and not app_name.startswith(" "):
        app_name = " {}".format(app_name)

    with default_transient_progress() as progress:
        progress.add_task("Installing{}...".format(app_name), start=False)

        if not dir_path.exists():
            raise LocationDoesNotExist("{} does not exist".format(dir_path))

        if not dir_path.is_dir():
            raise NotADirectory("{} is not a directory".format(dir_path))

        args = ["make", "install"] + args
        result = subprocess.run(args, cwd=dir_path, capture_output=True, text=True)

    if result.returncode == 0:
        console.print("Installing{}...[bold green]Done![/]".format(app_name))

    return result.returncode, result.stdout, result.stderr
