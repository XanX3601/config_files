import click
import git
import os
import pathlib
import rich.pretty as pretty
import rich.progress as progress
import subprocess
import shutil

pretty.install()

current_path = pathlib.Path('.')
home_path = pathlib.Path.home()
local_path = home_path.joinpath('local')
config_path = home_path.joinpath('.config')
config_bash_path = '$HOME/.config'
bashrc_path = home_path.joinpath('.bashrc')
bashrc_config_path = config_path.joinpath('bashrc')


@click.group()
def install():
    pass


@install.command()
def neovim():
    # clone repository
    with progress.Progress('[progress.description]{task.description}',
                           progress.BarColumn()) as prog:
        task = prog.add_task('Cloning neovim repository', start=False)

        nvim_repo_path = home_path.joinpath('neovim')

        if nvim_repo_path.exists():
            try:
                nvim_repo = git.Repo(nvim_repo_path)
            except:
                exit(1)
        else:
            nvim_repo = git.Repo.clone_from(
                'https://github.com/neovim/neovim.git', nvim_repo_path)

    # update local repository
    origin = nvim_repo.remotes.origin
    origin.pull()

    # make and install from local repository
    nvim_install_path = local_path.joinpath('neovim')

    nvim_build_path = nvim_repo_path.joinpath('build')

    if nvim_build_path.exists():
        shutil.rmtree(nvim_build_path)

    args = ['make', 'CMAKE_INSTALL_PREFIX={}'.format(nvim_install_path)]
    subprocess.run(args, cwd=nvim_repo_path)

    args = ['make', 'install']
    subprocess.run(args, cwd=nvim_repo_path)

    # install bash config
    nvim_bashrc_config_path = current_path.joinpath('neovim/bash_nvim')

    if not bashrc_config_path.exists():
        os.mkdir(bashrc_config_path)

    shutil.copy(nvim_bashrc_config_path, bashrc_config_path)

    bashrc_nvim_line = 'source {}/{}/bash_nvim'.format(config_bash_path,
                                                       bashrc_config_path.name)
    bash_nvim_line_found = False

    with open(bashrc_path, 'r') as bashrc:
        for line in bashrc:
            line = line.strip()
            if line == bashrc_nvim_line:
                bash_nvim_line_found = True

    if not bash_nvim_line_found:
        with open(bashrc_path, 'a') as bashrc:
            bashrc.write('# nvim config\n')
            bashrc.write('{}\n'.format(bashrc_nvim_line))

    # install nvim.init
    nvim_config_path = config_path.joinpath('nvim')

    if not config_path.exists():
        os.mkdir(nvim_config_path)

    if not nvim_config_path.exists():
        os.mkdir(nvim_config_path)

    nvim_init_path = current_path.joinpath('neovim/init.vim')

    shutil.copy(nvim_init_path, nvim_config_path)


@install.command()
def vifm():
    click.echo('installing vifm')


if __name__ == '__main__':
    install()
