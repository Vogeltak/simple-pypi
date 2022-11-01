from pathlib import Path
import os
import re
from subprocess import check_call
import sys

import click

from simple_pypi import index


def download_packages(target: Path, requirements: Path, packages: tuple[str]):
    """Download packages using pip-download."""
    if not requirements and not packages:
        click.secho("No packages to download", fg="blue")
        return

    cmd = [sys.executable, "-m", "pip", "download"]
    cmd += ["--dest", str(target.absolute())]

    if requirements:
        cmd += ["-r", str(requirements.absolute())]

    if packages:
        cmd += packages

    check_call(cmd)


def update_simple_repository(target: Path):
    """Establish repository entries for all packages at the target."""
    simple = target.joinpath("simple")
    simple.mkdir(mode=0o755, exist_ok=True)

    # Get a list of all downloaded archives at the top level.
    # This might include multiple versions or variants of the same package.
    wheel_list = list(target.glob("*.whl"))
    tar_list = list(target.glob("*.tar.gz"))

    pkg_names = [p.name.split("-")[0] for p in wheel_list]
    pkg_names += [p.name.rsplit("-", 1)[0] for p in tar_list]
    pkg_names = set(pkg_names)
    normalized_pkg_names = [normalize(p) for p in pkg_names]

    # Create top-level index for the repository

    top_level = index.Index(normalized_pkg_names)

    with open(simple.joinpath("index.html"), "w") as f:
        f.write(top_level.to_html())

    # Create index for every individual package

    for pkg in pkg_names:
        pkg_files = list(target.glob(f"{pkg}-*"))
        pkg_dir = simple.joinpath(normalize(pkg))
        pkg_dir.mkdir(mode=0o755, exist_ok=True)

        # Symlink all package files into the package index
        for f in pkg_files:
            try_symlink(f"../../{f.name}", pkg_dir.joinpath(f.name))

        # Create package index
        package_index = index.FileIndex(
            name=pkg,
            files={f.name: index.Hash.of("sha256", f) for f in pkg_files}
        )

        with open(pkg_dir.joinpath("index.html"), "w") as f:
            f.write(package_index.to_html())


def try_symlink(source: str, target: Path):
    try:
        os.symlink(source, target)
    except OSError as e:
        if e.errno == 17:
            # Ignore errors when file already exists
            return
        click.secho(f"Failed to symlink {target.name}: {e}", fg="red")
       

def normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def get_index_info(target: Path) -> int:
    """Parse target repository index to return general information."""
    simple_index = target.joinpath('simple/index.html')

    if not simple_index.exists():
        return None

    with open(simple_index, 'r') as f:
        html = f.read()

    parsed_index = index.Index.parse(html)

    return len(parsed_index.packages)
