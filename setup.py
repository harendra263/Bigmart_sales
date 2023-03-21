import pathlib
from setuptools import find_packages, setup
from typing import List

HYPEN_DOT_E = "-e ."

def get_requirements(filepath: str) -> List[str]:  # sourcery skip: path-read
    with open(file=filepath) as f:
        raw = f.read()
    requirements = list(raw.splitlines())
    if HYPEN_DOT_E in requirements:
        requirements.remove(HYPEN_DOT_E)
    return requirements


setup(
    name='Bigmart',
    version='0.0.1',
    author='Harendra kumar',
    author_email= 'harendra263@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt')
)

    