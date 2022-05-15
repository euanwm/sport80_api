""" Setup file for PyPi """
from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as readme_file:
    README = readme_file.read()

setup(
    name="sport80",
    version="2.1.0",
    description="Python API interface for the Sport80 sites",
    long_description=README,
    url="https://github.com/euanwm/sport80_api",
    author="Euan Meston",
    author_email="euanmeston@gmail.com",
    license="BSD",
    install_requires=["requests",
                      "beautifulsoup4",
                      "js2py"],
    classifiers=["Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9"],
    python_requires='>=3.8'
)
