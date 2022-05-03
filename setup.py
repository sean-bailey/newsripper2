from __future__ import absolute_import
from __future__ import print_function
from setuptools import setup, find_packages
import distutils.text_file
from pathlib import Path
from typing import List
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call

# Always prefer setuptools over distutils
import setuptools

class PreDevelopCommand(develop):
    """Pre-installation for development mode."""
    def run(self):
        check_call("pip3 install https://github.com/sean-bailey/Search-Engines-Scraper/archive/refs/heads/master.zip".split())
        develop.run(self)

class PreInstallCommand(install):
    """Pre-installation for installation mode."""
    def run(self):
        check_call("pip3 install https://github.com/sean-bailey/Search-Engines-Scraper/archive/refs/heads/master.zip".split())
        install.run(self)

def _parse_requirements(filename: str) -> List[str]:
    """Return requirements from requirements file."""
    # Ref: https://stackoverflow.com/a/42033122/
    return distutils.text_file.TextFile(filename=str(Path(__file__).with_name(filename))).readlines()

with open("README.md", "r") as fh:
    long_description = fh.read()
PreInstallCommand.run()
print(find_packages())

setup(
    name='newsripper',
    version='0.1.0a',
    packages=find_packages(),

    author="Sean Bailey",
    author_email="seanbailey518@gmail.com",
    description="This provides a utility to scrape and analyze news from around the internet",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sean-bailey",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
    ],
install_requires=_parse_requirements('REQUIREMENTS.txt'),

)

