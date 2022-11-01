from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
import re
import urllib.parse
from textwrap import indent


@dataclass
class Index:
    packages: list[str]

    @classmethod
    def parse(cls, html: str) -> Index:
        packages = re.findall(r'<a href=".+">(.+)</a>', html)
        return cls(packages)

    def to_html(self) -> str:
        links = "<br>\n".join(
            f'<a href="{name}/">{name}</a>'
            for name in sorted(self.packages)
        )

        return index_html.format(links=indent(links, " " * 4))


index_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Simple index</title>
  </head>
  <body>
{links}
  </body>
</html>
""".strip()


@dataclass
class Hash:
    name: str
    value: str

    @classmethod
    def of(cls, name: str, path: Path) -> Hash:
        h = hashlib.new(name)
        with open(path, "rb") as f:
            while True:
                block = f.read(0x10000)
                if not block:
                    break
                h.update(block)
        return cls(name, h.hexdigest())


@dataclass
class FileIndex:
    name: str
    files: dict[str, Hash]

    def to_html(self) -> str:
        links = "<br>\n".join(
            f'<a href="{urllib.parse.quote(file_name)}'
            + (f"#{file_hash.name}={file_hash.value}" if file_hash else "")
            + f'">{file_name}</a>'
            for file_name, file_hash in sorted(self.files.items())
        )

        return links_html.format(
            package_name=self.name,
            links=indent(links, " " * 4)
        )


links_html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Links for {package_name}</title>
  </head>
  <body>
    <h1>Links for {package_name}</h1>
{links}
  </body>
</html>
""".strip()
