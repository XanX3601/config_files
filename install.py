import click

from commands import (autoconf, automake, bash, cmake, libtool, llvm, ncurses,
                      neovim, node, openssl, vifm)
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
    cli.add_command(bash)
    cli.add_command(node)
    cli.add_command(cmake)
    cli.add_command(openssl)
    cli.add_command(llvm)
    cli()
