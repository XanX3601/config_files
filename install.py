import click

from commands import neovim, create_utils_dirs, vifm, libtool, automake, autoconf


@click.group()
def cli():
    pass


if __name__ == "__main__":
    create_utils_dirs()
    cli.add_command(neovim)
    cli.add_command(vifm)
    cli.add_command(libtool)
    cli.add_command(automake)
    cli.add_command(autoconf)
    cli()
