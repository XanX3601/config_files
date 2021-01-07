import shutil
import subprocess

from ..resources import console, default_transient_progress


def is_callable(command):
    """Check if a command is callable as a subprocess.

    Args:
        command (str): the name of the command

    Returns:
        bool: True if the command exists, false otherwise
    """
    return shutil.which(command) is not None


def call_command(args, command_name=""):
    """Invoke a command in the given directory.

    Args:
        args (list): the arguments used to run the command. It must be a list of string containing all arguments that must be passed to the command. The first being the name of the command it self.
        command_name (str): the name of the command. It is used in printed messages only.

    Returns:
        int: the return code of the command. If it is different than zero then something went wrong.
        str: the standard output of the command.
        str: the standard error output of the command.
    """
    if command_name != "" and not command_name.endswith(" "):
        command_name = "{} ".format(command_name)

    with default_transient_progress() as progress:
        progress.add_task("Calling {}command...".format(command_name), start=False)

        result = subprocess.run(args, capture_output=True, text=True)

    if result.returncode == 0:
        console.print("Calling {} command...[bold green]Done![/]".format(command_name))

    return result.returncode, result.stdout, result.stderr
