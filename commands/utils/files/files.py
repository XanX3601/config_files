"""Files functions."""

import os
import pathlib
import shutil
import tarfile

import requests

from ..resources import (console, default_transient_progress,
                         resources_dir_paths)


def create_directory(dir_path):
    """Create an empty directory.

    Args:
        dir_path (Path): the directory to create
    """
    console.print("Creating directory {}...".format(dir_path), end="")
    os.mkdir(dir_path)
    console.print("[bold green]Done![/]")


def create_resources_dirs():
    """Create the directories used in the installation scripts."""
    for dir_path in resources_dir_paths:
        if not dir_path.exists():
            create_directory(dir_path)


def download_archive(archive_link, archive_path, archive_name=""):
    """Download an archive or binary file.

    Args:
        archive_link (str): the archive's link
        archive_path (Path): where to download the archive
        archive_name (str): the name of the archive. It is used in printed
            messages only.
    """
    if archive_name != "" and not archive_name.endswith(" "):
        archive_name = "{} ".format(archive_name)

    with open(archive_path, "wb") as archive:
        with default_transient_progress() as progress:
            task_id = progress.add_task(
                "Downloading {}archive...".format(archive_name), start=False
            )

            response = requests.get(
                archive_link, stream=True, headers={"Accept-Encoding": ""}
            )
            total = int(response.headers.get("Content-Length"))

            progress.update(task_id, total=total)
            progress.start_task(task_id)

            for data in response.iter_content(chunk_size=1024):
                archive.write(data)
                progress.advance(task_id, len(data))

    console.print("Downloading {}archive...[bold green]Done![/]".format(archive_name))


def download_file(file_link, file_path, file_name=""):
    """Download a file.

    Args:
        file_link (str): the file's link
        file_path (Path): where to download the file
        file_name (str): the name of the file. It is used in printed messages only.
    """
    if file_name != "" and not file_name.endswith(" "):
        file_name = "{} ".format(file_name)

    with open(file_path, "wb") as file:
        with default_transient_progress() as progress:
            progress.add_task("Downloading {}file...".format(file_name), start=False)

            response = requests.get(file_link)
            file.write(response.content)

    console.print("Downloading {}file...[bold green]Done![/]".format(file_name))


def extract_tarfile(tarfile_path, tarfile_target, tarfile_name=""):
    """Extract a tarfile to the given target.

    Args:
        tarfile_path (Path): the location of the tarfile
        tarfile_target (Path): where to extract the tarfile
        tarfile_name (str): the name of the extracted tarfile, used in printed
            messages only.
    """
    if tarfile_name != "" and not tarfile_name.endswith(" "):
        tarfile_name = "{} ".format(tarfile_name)

    with default_transient_progress() as progress:
        progress.add_task("Extracting {}tarfile...".format(tarfile_name), start=False)

        with tarfile.open(tarfile_path) as tar:
            tar.extractall(tarfile_target)

    console.print("Extracting {}tarfile...[bold green]Done![/]".format(tarfile_name))


def move(source, target, source_name="", force=False):
    """Move source to target.

    Args:
        source (Path): the source to move.
        target (Path): where to move the source to.
        force (boolean): wether the move should overwrite files in destination.
        source_name (str): the name of the sourse, used in printed messages only.
    """

    def move_force(source, target):
        for dirpath, dirnames, filenames in os.walk(source):
            src_dir = pathlib.Path(dirpath)
            dest_dir = pathlib.Path(dirpath.replace(str(source), str(target), 1))

            if not dest_dir.exists():
                create_directory(dest_dir)

            for file in filenames:
                src = src_dir.joinpath(file)
                dst = dest_dir.joinpath(file)
                shutil.move(src, dst)

    if source_name != "" and not source_name.startswith(" "):
        source_name = " {}".format(source_name)

    with default_transient_progress() as progress:
        progress.add_task("Moving{}...".format(source_name), start=False)

        if not force:
            shutil.move(str(source), target)
        else:
            move_force(source, target)

    console.print("Moving{}...[bold green]Done![/]".format(source_name))


def remove(source, source_name=""):
    """Remove a source.

    Args:
        source (Path): the source to remove
        source_name (str): the name of the source, used in printed messages only.
    """
    if source_name != "" and not source_name.startswith(" "):
        source_name = " {}".format(source_name)

    with default_transient_progress() as progress:
        progress.add_task("Removing{}...".format(source_name), start=False)

        if source.is_dir():
            shutil.rmtree(source)
        else:
            source.unlink()

    console.print("Removing{}...[bold green]Done![/]".format(source_name))


def copy(source, target, source_name=""):
    """Copy source to target.

    Args:
        source (Path): the source to copy
        target (Path): where to copy the source
        source_name (str): the name of the sourse, used in printed messages only.
    """
    if source_name != "" and not source_name.startswith(" "):
        source_name = " {}".format(source_name)

    with default_transient_progress() as progress:
        progress.add_task("Copying{}...".format(source_name), start=False)

        shutil.copy(source, target)

    console.print("Copying{}...[bold green]Done![/]".format(source_name))
