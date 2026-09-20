"""Generate the pinned schema immediately before packaging; never commit it."""

from pathlib import Path
import subprocess
import sys

from setuptools import setup
from setuptools.command.build_py import build_py


class BuildPy(build_py):
    def run(self):
        subprocess.run([sys.executable, str(Path(__file__).parent / "tools" / "sync_schema.py")], check=True)
        super().run()


setup(cmdclass={"build_py": BuildPy})
