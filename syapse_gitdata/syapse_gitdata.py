# -*- coding: utf-8 -*-
"""Main module."""
from syapse_gitdata.api_accessor import Accessor
from syapse_gitdata.structlogger import structlog
from syapse_gitdata.writer import *
import os


LOG = structlog.get_logger()

class GitData():
    def __init__(self, token):
        self._token = token

    def collect_metrics(self, file_type) -> None:
        """Collects raw data on PullRequests that a user can access."""
        user = Accessor(self._token)
        try:
            repos = user.get_repos()
        except KeyError:
            repos = user.get_repos()
        for r in repos:
            LOG.info("Repository: "+str(r))
            prs = r.get_pull_requests()
            if os.path.exists('syapse_gitdata/output.json'):
                update_json(prs)
            else:
                write_json(prs)
