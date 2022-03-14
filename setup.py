""" Setup file for PyPi """
from setuptools import setup

setup(
    name="pySport80",
    version="0.1.1",
    description="pyAPI for Sport80",
    url="https://github.com/euanwm/sport80_api",
    author="Euan Meston",
    author_email="euanmeston@gmail.com",
    license="MIT",
    install_requires=["requests",
                      "beautifulsoup4"],
    classifiers=["Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9"],
    python_requires='>=3.8'
)
