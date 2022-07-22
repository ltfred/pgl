import os
import pickle
import sys

import click
import toml


CONFIG_CONTENT = """
# gitlab domain, like https://gitlab.com
base_url = ""

# gitlab access token
token = ""

# gitlab project_dir
# default ./
project_dir = ""

# If set, pgl clone will auto set user.name in repo gitconfig
# default empty
name = ""

# If set, pgl clone will auto set user.email in repo gitconfig
# default empty
email = ""
"""


# pylint: disable=too-many-instance-attributes
class Config:
    """
    Config Class
    """

    def __init__(self):
        self.token = None
        self.base_url = None
        self.name = None
        self.email = None
        self.project_dir = None
        self.home = os.environ["HOME"]
        self.config_file_path = os.path.join(self.home, ".config", "pgl", "config.toml")
        self.project_file_path = os.path.join(self.home, ".config", "pgl", ".projects")
        self.check_config_file()

    def setup(self):
        """Setup config"""
        config = toml.load(self.config_file_path)
        self.base_url = config.get("base_url", "")
        if self.base_url == "":
            click.secho("Set Gitlab base url first, use `pgl config.`", fg="red")
            sys.exit()
        if not self.base_url.startswith("http"):
            self.base_url = "https://" + self.base_url
        if not self.base_url.endswith("/"):
            self.base_url = self.base_url + "/"
        self.token = config.get("token", "")
        if self.token == "":
            click.secho("Set Gitlab token first, use `lab config.`", fg="red")
            sys.exit()
        self.name = config.get("name", "")
        self.email = config.get("email", "")
        self.project_dir = config.get("project_dir", "")

    def create_config_file(self):
        """Create config file"""
        lab_dir = os.path.join(self.home, ".config", "pgl")
        if not os.path.isdir(lab_dir):
            os.makedirs(lab_dir)
        with open(self.config_file_path, "w", encoding="utf-8") as writer:
            writer.write(CONFIG_CONTENT)

    def check_config_file(self):
        """Check config file"""
        if not os.path.isfile(self.config_file_path):
            self.create_config_file()

    def read_project_file(self):
        """Read projects"""
        with open(self.project_file_path, "rb") as file:
            return pickle.load(file)

    def write_project_file(self, path_with_namespace):
        """Write projects"""
        with open(self.project_file_path, "wb") as file:
            pickle.dump(path_with_namespace, file)
