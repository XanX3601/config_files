import click
import git
import pathlib
import subprocess

home_path = pathlib.Path.home()
local_path = home_path.joinpath('local')
bashrc_path = home_path.joinpath('.bashrc')
bashrc_config_path = 


@click.group()
def install():
    pass


@install.command()
def neovim():
    # clone repository
    nvim_repo_path = home_path.joinpath('neovim')

    if nvim_repo_path.exists():
        try:
            git.Repo(nvim_repo_path)
        except:
            exit(1)
    else:
        git.Repo.clone_from('https://github.com/neovim/neovim.git',
                            nvim_repo_path)

    # make and install from local repository
    nvim_install_path = local_path.joinpath('nvim')

    args = ['make', 'CMAKE_INSTALL_PREFIX={}'.format(nvim_install_path)]
    subprocess.run(args, cwd=nvim_repo_path)

    args = ['make', 'install']
    subprocess.run(args, cwd=nvim_repo_path)

    # add config to bashrc


@install.command()
def vifm():
    click.echo('installing vifm')


if __name__ == '__main__':
    install()
