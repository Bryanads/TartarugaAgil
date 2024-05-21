# setup.py
from setuptools import setup, find_packages


setup(
    name="tartaruga",
    version="0.1.0",
    description="Managing tool for SCRUM teams",
    author="Tartaruga Agil",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "tartaruga = tartaruga.__main__:main"
        ]
    }
    
)