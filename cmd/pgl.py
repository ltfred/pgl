import asyncio
import os
import sys

import click
import prompt_toolkit
from prompt_toolkit.completion import WordCompleter

from internal.config import Config
from cmd import __version__
from internal.lab import Lab
from utils.display import output


class PGL:

    def __init__(self):
        self.cf = Config()

    @staticmethod
    def version():
        click.echo(__version__)
        sys.exit()

    def config(self):
        click.edit(filename=self.cf.config_file_path)
        sys.exit()

    def sync(self):
        self.cf.setup()
        lab = Lab(self.cf.base_url, self.cf.token)
        groups = lab.groups()
        projects = []
        tasks = [self.get_projects_by_group(lab, i, projects) for i in groups]
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = asyncio.wait(tasks)
        loop.run_until_complete(tasks)
        path_with_namespace = [p.path_with_namespace for p in projects]
        self.cf.write_project_file(path_with_namespace)
        sys.exit()

    @staticmethod
    async def get_projects_by_group(client, group, projects):
        projects.extend(client.projects_by_group(group))

    def clone(self):
        self.cf.setup()
        projects = self.cf.read_project_file()
        projects_completer = WordCompleter(projects, ignore_case=True, WORD=True, match_middle=True)
        project = prompt_toolkit.prompt("Enter or choose a project: ", completer=projects_completer)
        lab = Lab(self.cf.base_url, self.cf.token)
        project = lab.search_project(project.split("/")[1])
        if len(project) == 0:
            output("Not find project!")
        url = project[0]["ssh_url_to_repo"]
        os.system("git clone " + url)
        sys.exit()

