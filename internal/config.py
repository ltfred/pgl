import os
import pickle

import toml

from utils.display import output

CONFIG_CONTENT = """
# gitlab domain, like https://gitlab.com
base_url = ""

# gitlab access token
token = ""

# gitlab projects file
# default $HOME/lab/projects
projects = ""

# If set, lab clone will auto set user.name in repo gitconfig
# default empty
name = ""

# If set, lab clone will auto set user.email in repo gitconfig
# default empty
email = ""
"""


class Config:
    """
    Config Class
    """

    def __init__(self):
        self.token = None
        self.base_url = None
        self.home = os.environ["HOME"]
        self.config_file_path = os.path.join(self.home, ".config", "pgl", "config.toml")
        self.project_file_path = os.path.join(self.home, ".config", "pgl", ".projects")
        self.check_config_file()

    def setup(self):
        config = toml.load(self.config_file_path)
        self.base_url = config.get("base_url", "")
        if self.base_url == "":
            output("Set Gitlab base url first, use `pgl config.`")
        if not self.base_url.startswith("http"):
            self.base_url = "https://" + self.base_url
        self.token = config.get("token", "")
        if self.token == "":
            output("Set Gitlab token first, use `lab config.`")
        self.check_project_file()

    def create_config_file(self):
        lab_dir = os.path.join(self.home, ".config", "pgl")
        if not os.path.isdir(lab_dir):
            os.makedirs(lab_dir)
        with open(self.config_file_path, "w", encoding="utf-8") as writer:
            writer.write(CONFIG_CONTENT)

    def check_config_file(self):
        if not os.path.isfile(self.config_file_path):
            self.create_config_file()

    def check_project_file(self):
        if not os.path.isfile(self.project_file_path):
            self.create_project_file()

    def read_project_file(self):
        with open(self.project_file_path, "rb") as file:
            return pickle.load(file)

    def write_project_file(self, path_with_namespace):
        with open(self.project_file_path, "wb") as file:
            pickle.dump(path_with_namespace, file)

    def create_project_file(self):
        open(self.project_file_path, "w").close()
