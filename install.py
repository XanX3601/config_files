import click

from commands import neovim, create_utils_dirs, vifm, libtool


@click.group()
def cli():
    pass


if __name__ == "__main__":
    create_utils_dirs()
    cli.add_command(neovim)
    cli.add_command(vifm)
    cli.add_command(libtool)
    cli()
