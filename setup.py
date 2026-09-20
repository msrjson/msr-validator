"""Generate the pinned schema immediately before packaging; never commit it."""

from pathlib import Path
import subprocess
import sys

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info


def sync_schema() -> None:
    subprocess.run([sys.executable, str(Path(__file__).parent / "tools" / "sync_schema.py")], check=True)


class BuildPy(build_py):
    def run(self):
        sync_schema()
        super().run()


class EggInfo(egg_info):
    def run(self):
        sync_schema()
        super().run()


setup(cmdclass={"build_py": BuildPy, "egg_info": EggInfo})
