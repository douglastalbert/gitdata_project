import requests
import datetime
from syapse_gitdata.repository import Repository
from typing import List, Dict

class PullRequest():

    def __init__(self, url, header):
        self._header = header
        self.url = url
        self._id = None
        self.user = None
        self.state = None
        self.created = None
        self.updated = None
        self.closed = None
        self.assignees = None
        self.reviewers = None
        self.review_teams = None
        self.labels = None
        self.branch = None
        self.merged = None
        self.comments = None
        self.review_comments = None
        self.commits = None
        self.additions = None
        self.deletions = None
        self.changed_files = None
        self._json = requests.get(self.url, headers=self._header).json()
        self.repo = None

    def parse_json(self) -> None:
        """Parses the JSON data in self._json to assign object properties."""
        self._id = self._json['id']
        self.user =self._json['user']['login']
        self.state = self._json['state']
        self.updated = datetime.datetime.strptime(self._json['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        self.assignees = self._json['assignees']
        self.reviewers = self._json['requested_reviewers']
        self.review_teams = self._json['requested_teams']
        self.labels = self._json['labels']
        self.branch = self._json['head']['ref']
        self.merged = self._json['merged']
        self.comments = self._json['comments']
        self.review_comments = self._json['review_comments']
        self.commits = self._json['commits']
        self.additions = self._json['additions']
        self.deletions = self._json['deletions']
        self.changed_files = self._json['changed_files']
        created = self._json['created_at']
        self.created = datetime.datetime.strptime(created, '%Y-%m-%dT%H:%M:%SZ')
        closed = self._json['closed_at']
        if closed is not None:
            self.closed = datetime.datetime.strptime(closed, '%Y-%m-%dT%H:%M:%SZ')
        r = Repository(self._json['head']['repo']['url'], self._header)
        r.parse_json()
        self.repo=r

    def login_only(self,user_list) -> List[str]:
        """Helper method that extracts the login from a JSON object."""
        logins = []
        for user in user_list:
            logins.append(user['login'])
        return logins

    def name_only(self,team_list) -> List[str]:
        """Helper method that extracts the name from a JSON object."""
        names = []
        for team in team_list:
            names.append(team['name'])
        return names

    def csv_format(self) -> List[str]:
        """Returns the csv row representation of a PullRequest."""
        if self.closed is not None:
            return [self.repo.name,self.user,self.state,self.url,\
                    self.created.strftime('%Y-%m-%dT%H:%M:%SZ'),self.updated.strftime('%Y-%m-%dT%H:%M:%SZ'),\
                    self.closed.strftime('%Y-%m-%dT%H:%M:%SZ'),str(self.login_only(self.assignees)),str(self.login_only(self.reviewers)),\
                    str(self.name_only(self.review_teams)),str(self.name_only(self.labels)),self.branch,self.merged,self.comments,\
                    self.review_comments,self.commits,self.additions,self.deletions,self.changed_files]
        else:
            return [self.repo.name,self.user,self.state,self.url,\
                    self.created.strftime('%Y-%m-%dT%H:%M:%SZ'),self.updated.strftime('%Y-%m-%dT%H:%M:%SZ'),\
                    '',str(self.login_only(self.assignees)),str(self.login_only(self.reviewers)),\
                    str(self.name_only(self.review_teams)),str(self.name_only(self.labels)),self.branch,self.merged,self.comments,\
                    self.review_comments,self.commits,self.additions,self.deletions,self.changed_files]

    def json_format(self) -> Dict:
        """Returns a dictionary representation of the PR to be converted to json."""
        dict_rep = {}
        dict_rep['repo'] = self.repo.name
        dict_rep['user'] = self.user
        dict_rep['state'] = self.state
        dict_rep['url'] = self.url
        dict_rep['created'] = self.created.strftime('%Y-%m-%dT%H:%M:%SZ')
        dict_rep['updated'] = self.updated.strftime('%Y-%m-%dT%H:%M:%SZ')
        if self.closed is not None:
            dict_rep['closed'] = self.closed.strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            dict_rep['closed'] = None
        dict_rep['assignees'] = self.login_only(self.assignees)
        dict_rep['reviewers'] = self.login_only(self.reviewers)
        dict_rep['review_teams'] = self.name_only(self.review_teams)
        dict_rep['labels'] = self.name_only(self.labels)
        dict_rep['branch'] = self.branch
        dict_rep['merged'] = self.merged
        dict_rep['comments'] = self.comments
        dict_rep['review_comments'] = self.review_comments
        dict_rep['commits'] = self.commits
        dict_rep['additions'] = self.additions
        dict_rep['deletions'] = self.deletions
        dict_rep['changed_files'] = self.changed_files
        return dict_rep

    def __str__(self) -> str:
        return "State: {a}, Repository: {b}, User: {c}".format(a=self.state, c=self.user, b=self.repo.name)
