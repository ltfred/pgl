from setuptools import setup, find_packages
import cmd

setup(
    name="pgl",
    version=cmd.__version__,
    author="ltfred",
    author_email="ltfred@163.com",
    description="A command-line tool for gitlab",
    url="https://github.com/ltfred/pgl",
    install_requires=[
        'click',
        "toml",
        "prompt_toolkit",
        "python-gitlab"
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pgl=cmd.root:pgl'
        ]
    },
)