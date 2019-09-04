"""
    Class for accessing repositories
"""

import json

import requests
from syapse_gitdata.repository import Repository
from syapse_gitdata.pull import PullRequest
from syapse_gitdata.structlogger import structlog
from typing import List

USER_PATH = 'https://api.github.com/user'
REPOS_PATH = USER_PATH + '/repos'

LOG = structlog.get_logger()

class Accessor():
    def __init__(self, token):
        self._token = token
        self._header = {'Authorization': 'token '+token}
        self._json = None
        self.name = None
        self._id = None

        self.repos = None

    def authenticate(self) -> None:
        """Calls the Github API and parses the response to access API response"""
        self._json = requests.get(USER_PATH, headers=self._header).json()
        assert('message' not in self._json.keys()), 'Invalid Token'
        self._parse_json(self._json)

    def _parse_json(self, response) -> None:
        """Parses the JSON data in self._json to assign object properties."""
        self.name = self._json['login']
        LOG.info("Parsing user json...")
        self._id = self._json['id']

    @staticmethod
    def get_digits(enclosing_string, index):
        """Helper method for retreiving number of digits of int enclosed in str."""
        digit = 1
        while True:
            if enclosing_string[index + digit : index + digit + 1].isdigit():
                digit += 1
            else:
                break
        return digit

    def get_repos(self) -> List[Repository]:
        """Returns a list of the Repository objects that this user can access."""
        repositories = []
        repo_return = requests.get(REPOS_PATH, headers=self._header)
        head = repo_return.headers
        repo_list = repo_return.json()
        LOG.info("Getting repositories...")

        for repo in self.get_page_repos(repo_list):
            repositories.append(repo)
        if "Link" not in head.keys():
            LOG.info("One Page")
            for repo in self.get_page_repos(repo_list):
                repositories.append(repo)
        else:
            LOG.info("Paginated Response")
            link = head['Link']
            assert('last' in link), """Link format does not contain '<URL>; rel="last"'"""
            num_pages_index = int(link.index('rel="last"')) - 5
            pages = int(link[num_pages_index : num_pages_index + Accessor.get_digits(link, num_pages_index)])
            for repo in self.get_page_repos(repo_list):
                repositories.append(repo)
            page = 2
            while page <= pages:
                path = REPOS_PATH + '?page=' + str(page)
                repo_list = requests.get(path, headers=self._header).json()
                for repo in self.get_page_repos(repo_list):
                    if repo.name != 'Documentation' and repo.name != 'lab-integration-serverless':
                        repositories.append(repo)
                page += 1
        self.repos = repositories
        if len(self.repos) == 0:
            LOG.warning("No repositories found")
        return repositories

    def get_page_repos(self, repo_list) -> List[Repository]:
        """Helper method for retreiving repositories from a paginated response."""
        repositories=[]

        for repo in repo_list:
            r = Repository(repo['url'],self._header)
            r.parse_json()
            repositories.append(r)
        return repositories




    def get_pull_requests(self,repo_name) -> List[PullRequest]:
        """Returns a list of the PullRequests in the specified Repository."""
        for repo in self.repos:
            if repo_name == repo.name:
                return repo.get_pull_requests()
        LOG.error("No matching repositories found")

    def all_pull_requests(self) -> List[PullRequest]:
        """Returns a list of all PullRequests that the user can access."""
        pull_requests = []
        repos = self.get_repos()
        LOG.info("Getting pull requests...")
        for repo in repos:
            for pr in self.get_pull_requests(repo.name):
                pull_requests.append(pr)
        return pull_requests
