import click

from commands import neovim, vifm, ncurses, automake, autoconf, libtool
from commands.utils.files import create_resources_dirs


@click.group()
def cli():
    pass


if __name__ == "__main__":
    create_resources_dirs()
    cli.add_command(neovim)
    cli.add_command(libtool)
    cli.add_command(autoconf)
    cli.add_command(automake)
    cli.add_command(vifm)
    cli.add_command(ncurses)
    cli()
