import asyncio
import os
import subprocess
import sys

import click
import prompt_toolkit
from prompt_toolkit.completion import WordCompleter

from internal.config import Config
from internal.lab import Lab


class PGL:
    """
    PGL Class
    """

    def __init__(self):
        # pylint: disable=invalid-name
        self.cf = Config()

    def config(self):
        """Edit config file"""
        click.edit(filename=self.cf.config_file_path)
        sys.exit()

    def sync(self):
        """Sync projects"""
        self.cf.setup()
        lab = Lab(self.cf.base_url, self.cf.token)
        click.secho("Syncing......", fg="green")
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
        """Get project by group"""
        projects.extend(client.projects_by_group(group))

    def clone(self):
        """Clone project"""
        self.cf.setup()
        project = self.prompt()
        lab = Lab(self.cf.base_url, self.cf.token)
        project = lab.search_project(project.split("/")[-1])
        if len(project) == 0:
            click.secho("Not find project!", fg="yellow")
            sys.exit()
        url = project[0]["ssh_url_to_repo"]
        path = os.path.join(self.cf.project_dir, project[0]['name']) \
            if self.cf.project_dir else os.path.join(os.getcwd(), project[0]['name'])
        subprocess.call(["git", "clone", url, path])
        os.chdir(path)
        if self.cf.name != "":
            os.system(f"git config user.name {self.cf.name}")
        if self.cf.email != "":
            os.system(f"git config user.email {self.cf.email}")
        sys.exit()

    def prompt(self):
        """Project prompt"""
        projects = self.cf.read_project_file()
        projects_completer = WordCompleter(projects, ignore_case=True, WORD=True, match_middle=True)
        return prompt_toolkit.prompt("Enter or choose a project: ", completer=projects_completer)

    def browser(self, pipeline):
        """Open project in web browser"""
        self.cf.setup()
        project = self.prompt()
        url = self.cf.base_url + project
        if pipeline:
            url = url + "/-/pipelines"
        click.launch(url)
        sys.exit()
