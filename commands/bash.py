import click

from .utils.files import copy
from .utils.print import print_msg_titled
from .utils.resources import configs_path, home_path

bash_name = "bash"
bash_bashrc_path = configs_path.joinpath("bash/bashrc")
bash_config_path = home_path.joinpath(".bashrc")


@click.group()
def bash():
    """bash commands group."""
    pass


@bash.command()
def info():
    """print info on bash."""
    print_msg_titled(bash_name, "only install a bashrc file.")


@bash.command()
def install():
    """install bash locally."""
    # copy bashrc
    copy(
        bash_bashrc_path, bash_config_path, "{} {}".format(bash_name, bash_bashrc_path)
    )
