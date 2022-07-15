import gitlab.const
from gitlab import Gitlab


class Lab:
    """
    Gitlab class
    """

    def __init__(self, base_url, token):
        self.client = Gitlab(base_url, token)

    def search_project(self, project_name):
        projects = []
        for project in self.client.search(gitlab.const.SEARCH_SCOPE_PROJECTS, project_name):
            if project["name"] == project_name:
                projects.append(project)
        return projects

    def get_group(self, group_name):
        return self.client.groups.get(group_name)

    def projects(self):
        projects = self.client.projects.list(all=True)
        return projects

    @staticmethod
    def projects_by_group(group):
        return group.projects.list(all=True)

    def groups(self):
        return self.client.groups.list(all=True)
