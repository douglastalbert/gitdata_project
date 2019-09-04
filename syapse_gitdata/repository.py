import requests
from syapse_gitdata.structlogger import structlog
from typing import List, Dict
import json
import os


LOG = structlog.get_logger()
RESULTS_PER_PAGE = "100"

class Repository():

    def __init__(self, url, header):
        self._url = url
        self._header = header
        self._id = None
        self.name = None
        self._json = requests.get(self._url, headers=self._header).json()
        self._pr_url = None

    def parse_json(self) -> None:
        """Parses the JSON data in self._json to assign object properties."""
        self._id = self._json['id']
        self.name = self._json['name']
        # Remove last 9 characters from 'pulls_url' in json
        # This is a generic ending meant to be replaced by the user
        # An api call to 'pulls_url' key returns https://api.github.com/repos/douglastalbert/demo/pulls{/number}
        # When {/number} is removed, a call to this returns all list of pull requests
        self._pr_url = self._json['pulls_url'][0:-9] + "?state=all&per_page=" + RESULTS_PER_PAGE

    def get_pull_requests(self) -> List:
        """Returns a list of the PullRequests in this Repository."""
        from syapse_gitdata.pull import PullRequest
        pull_requests = []
        if os.path.exists('syapse_gitdata/output.json'):
            pull_requests = self.get_changed_prs()
        else:
            for pr in requests.get(self._pr_url, headers=self._header).json():
                req = PullRequest(pr['url'],self._header)
                req.parse_json()
                pull_requests.append(req)

        return pull_requests

    def get_changed_prs(self) -> List:
        """Returns a list of pull requests that have been added or updated"""
        from syapse_gitdata.pull import PullRequest
        pull_requests = []
        with open('syapse_gitdata/output.json', 'r') as file_read:
            written_data = json.load(file_read)
            LOG.info('File Loaded Successfully')
            pr_dict = {}
            for pr in written_data:
                pr_dict.update({pr['url'] : pr})
            for pr in requests.get(self._pr_url, headers=self._header).json():
                if pr['url'] not in pr_dict.keys():
                    req = PullRequest(pr['url'],self._header)
                    req.parse_json()
                    pull_requests.append(req)
                elif pr['updated_at'] != pr_dict[pr['url']]['updated']:
                     req = PullRequest(pr['url'],self._header)
                     req.parse_json()
                     pull_requests.append(req)
            file_read.seek(0)
        return pull_requests

    def __str__(self) -> str:
        return self.name

    def json_format(self) -> Dict:
        """Returns a dictionary representation of the repo to be converted to json."""
        dict_rep = {}
        dict_rep['name'] = self.name
        dict_rep['pull_requests'] = {}
        count = 1
        for pr in self.get_pull_requests():
            dict_rep['pull_requests'][count] = str(pr)
            count += 1
        return dict_rep
