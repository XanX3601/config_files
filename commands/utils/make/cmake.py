import subprocess

from ..files import LocationDoesNotExist, NotADirectory
from ..resources import console, default_transient_progress


def cmake(dir_path, args, app_name=""):
    """Invoke cmake in the given directory.

    Args:
        dir_path (Path): the directory in which invoke cmake.
        args (list): the arguments to pass to cmake. It must be a list of string
            containing all arguments that must be passed to cmake.

    Returns:
        int: the return code of cmake. If it is different than zero then something
            went wrong.
        str: the standard output of cmake
        std: the standard error output of cmake

    Raises:
        LocationDoesNotExist: if the given directory does not exist.
        NotADirectory: if the given location is not a directory.
    """
    if app_name != "" and not app_name.startswith(" "):
        app_name = " {}".format(app_name)

    with default_transient_progress() as progress:
        progress.add_task("Cmaking{}...".format(app_name), start=False)

        if not dir_path.exists():
            raise LocationDoesNotExist("{} does not exist".format(dir_path))

        if not dir_path.is_dir():
            raise NotADirectory("{} is not a directory".format(dir_path))

        args = ["cmake"] + args
        result = subprocess.run(args, cwd=dir_path, capture_output=True, text=True)

    if result.returncode == 0:
        console.print("Cmaking{}...[bold green]Done![/]".format(app_name))

    return result.returncode, result.stdout, result.stderr
