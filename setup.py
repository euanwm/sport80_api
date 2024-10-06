""" Setup file for PyPi """
from setuptools import setup

setup(
    name="sport80",
    version="2.2.6",
    description="Python API interface for the Sport80 sites",
    long_description='Intentionally empty',
    url="https://github.com/euanwm/sport80_api",
    author="Euan Meston",
    author_email="euanmeston@gmail.com",
    license="BSD",
    install_requires=["requests",
                      "beautifulsoup4"],
    classifiers=["Programming Language :: Python :: 3.11"],
    python_requires='>=3.8'
)
