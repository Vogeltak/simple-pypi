# Simple PyPI

Create and manage Python package indexes conforming to the Simple Repository API ([PEP 503](https://peps.python.org/pep-0503/)).

## Usage

The main command is the `install` command.

```sh
$ simple-pypi install --help
Usage: simple-pypi install [OPTIONS] REPO [PACKAGES]...

  Pull requirements from PyPI into the target repository

  The repository path can either be local or remote. When the path contains
  ':', it is considered a remote path, and Simple PyPI will push to it using
  rsync.

Options:
  -r, --requirements PATH  Requirements.txt file
  --help                   Show this message and exit.
```

To create a new Python repository at `/tmp/pypi` and populate it from a requirements file, run

```sh
$ simple-pypi install /tmp/pypi -r requirements.txt
```

After it completes, `/tmp/pypi` will contain all packages at the top-level.
The PEP 503 repository is at `/tmp/pypi/simple`.
There will be directories for every individual package, and index files for navigation.

Use the repository:

```sh
$ pip install --index-url file:///tmp/pypi/simple httpx
Looking in indexes: file:///tmp/pypi/simple
Processing /tmp/pypi/simple/httpx/httpx-0.23.0-py3-none-any.whl
Processing /tmp/pypi/simple/certifi/certifi-2022.9.24-py3-none-any.whl
Processing /tmp/pypi/simple/rfc3986/rfc3986-1.5.0-py2.py3-none-any.whl
Processing /tmp/pypi/simple/httpcore/httpcore-0.15.0-py3-none-any.whl
Processing /tmp/pypi/simple/sniffio/sniffio-1.3.0-py3-none-any.whl
Processing /tmp/pypi/simple/anyio/anyio-3.6.2-py3-none-any.whl
Processing /tmp/pypi/simple/h11/h11-0.12.0-py3-none-any.whl
Processing /tmp/pypi/simple/idna/idna-3.4-py3-none-any.whl
Installing collected packages: rfc3986, sniffio, idna, h11, certifi, anyio, httpcore, httpx
Successfully installed anyio-3.6.2 certifi-2022.9.24 h11-0.12.0 httpcore-0.15.0 httpx-0.23.0 idna-3.4 rfc3986-1.5.0 sniffio-1.3.0
```
