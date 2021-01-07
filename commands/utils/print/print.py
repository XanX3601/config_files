from ..resources import console


def print_stdoutputs(title, stdout, stderr):
    """Print the outputs of a subprocess with a title in a rich console.

    Args:
        title (str): the title of the print
        stdout (str): the standard output to print
        stderr (str): the standard error output to print
    """
    console.print(title, justify="center")
    console.rule("stdout")
    console.print(stdout)
    console.rule("stderr")
    console.print(stderr)


def print_msg_titled(title, msg):
    """Print a message with a title

    Args:
        title (str): the title of the print
        msg (str): the message to print
    """
    console.print(title, justify="center")
    console.print(msg)
