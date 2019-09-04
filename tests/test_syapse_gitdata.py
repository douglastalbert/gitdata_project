#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `syapse_gitdata` package."""
import sys

print(sys.path)
#sys.path.append("/Users/dtalbert/Documents/syapse-gitdata/syapse_gitdata")
# sys.path.insert(0, '/path/to/syapse_gitdata')
# print(sys.path)
import pytest
import importlib
from click.testing import CliRunner
from unittest.mock import patch, Mock
from decouple import config
from syapse_gitdata import cli
from syapse_gitdata import syapse_gitdata
from pytest_mock import mocker
from syapse_gitdata.user import User
from syapse_gitdata.repository import Repository
from syapse_gitdata.pull import PullRequest
from syapse_gitdata.structlogger import structlog

LOG = structlog.get_logger()
TOKEN = "MY_TOKEN"

MOCK_HEADER = {'Authorization': 'token '+ TOKEN}
MOCK_URL = "https://api.github.com"

@pytest.mark.skip(reason="Will error out because it takes too long")
def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'syapse_gitdata.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

def test_correct_token_stored():
    u = User(TOKEN)
    assert TOKEN == u._token

def test_authenticate():
    user = {
            "login": "douglastalbert",
            "id": 35708020,
            "node_id": "MDQ6VXNlcjM1NzA4MDIw",
            "avatar_url": "https://avatars1.githubusercontent.com/u/35708020?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/douglastalbert",
            "html_url": "https://github.com/douglastalbert",
            "followers_url": "https://api.github.com/users/douglastalbert/followers",
            "following_url": "https://api.github.com/users/douglastalbert/following{/other_user}",
            "gists_url": "https://api.github.com/users/douglastalbert/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/douglastalbert/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/douglastalbert/subscriptions",
            "organizations_url": "https://api.github.com/users/douglastalbert/orgs",
            "repos_url": "https://api.github.com/users/douglastalbert/repos",
            "events_url": "https://api.github.com/users/douglastalbert/events{/privacy}",
            "received_events_url": "https://api.github.com/users/douglastalbert/received_events",
            "type": "User",
            "site_admin": False,
            "name": None,
            "company": None,
            "blog": "",
            "location": None,
            "email": None,
            "hireable": None,
            "bio": None,
            "public_repos": 3,
            "public_gists": 0,
            "followers": 0,
            "following": 0,
            "created_at": "2018-01-22T21:35:53Z",
            "updated_at": "2019-06-10T23:07:48Z",
            "private_gists": 0,
            "total_private_repos": 0,
            "owned_private_repos": 0,
            "disk_usage": 28,
            "collaborators": 0,
            "two_factor_authentication": True,
            "plan": {
                "name": "free",
                "space": 976562499,
                "collaborators": 0,
                "private_repos": 10000
            }
    }
    mock_get_user_patcher = patch("requests.get")
    mock_get_user = mock_get_user_patcher.start()
    mock_get_user.return_value.json.return_value = user

    u = User(TOKEN)
    u.authenticate()
    assert u._json is not None
    assert u.name == 'douglastalbert'
    assert u._id == 35708020
    mock_get_user.stop()
def test_repository_parse_json():
    repo = {
        "id": 191225856,
        "node_id": "MDEwOlJlcG9zaXRvcnkxOTEyMjU4NTY=",
        "name": "demo",
        "full_name": "douglastalbert/demo",
        "private": False,
        "owner": {
            "login": "douglastalbert",
            "id": 35708020,
            "node_id": "MDQ6VXNlcjM1NzA4MDIw",
            "avatar_url": "https://avatars1.githubusercontent.com/u/35708020?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/douglastalbert",
            "html_url": "https://github.com/douglastalbert",
            "followers_url": "https://api.github.com/users/douglastalbert/followers",
            "following_url": "https://api.github.com/users/douglastalbert/following{/other_user}",
            "gists_url": "https://api.github.com/users/douglastalbert/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/douglastalbert/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/douglastalbert/subscriptions",
            "organizations_url": "https://api.github.com/users/douglastalbert/orgs",
            "repos_url": "https://api.github.com/users/douglastalbert/repos",
            "events_url": "https://api.github.com/users/douglastalbert/events{/privacy}",
            "received_events_url": "https://api.github.com/users/douglastalbert/received_events",
            "type": "User",
            "site_admin": False
        },
        "html_url": "https://github.com/douglastalbert/demo",
        "description": "Demo from Udemy git/github course",
        "fork": False,
        "url": "https://api.github.com/repos/douglastalbert/demo",
        "forks_url": "https://api.github.com/repos/douglastalbert/demo/forks",
        "keys_url": "https://api.github.com/repos/douglastalbert/demo/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/douglastalbert/demo/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/douglastalbert/demo/teams",
        "hooks_url": "https://api.github.com/repos/douglastalbert/demo/hooks",
        "issue_events_url": "https://api.github.com/repos/douglastalbert/demo/issues/events{/number}",
        "events_url": "https://api.github.com/repos/douglastalbert/demo/events",
        "assignees_url": "https://api.github.com/repos/douglastalbert/demo/assignees{/user}",
        "branches_url": "https://api.github.com/repos/douglastalbert/demo/branches{/branch}",
        "tags_url": "https://api.github.com/repos/douglastalbert/demo/tags",
        "blobs_url": "https://api.github.com/repos/douglastalbert/demo/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/douglastalbert/demo/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/douglastalbert/demo/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/douglastalbert/demo/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/douglastalbert/demo/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/douglastalbert/demo/languages",
        "stargazers_url": "https://api.github.com/repos/douglastalbert/demo/stargazers",
        "contributors_url": "https://api.github.com/repos/douglastalbert/demo/contributors",
        "subscribers_url": "https://api.github.com/repos/douglastalbert/demo/subscribers",
        "subscription_url": "https://api.github.com/repos/douglastalbert/demo/subscription",
        "commits_url": "https://api.github.com/repos/douglastalbert/demo/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/douglastalbert/demo/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/douglastalbert/demo/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/douglastalbert/demo/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/douglastalbert/demo/contents/{+path}",
        "compare_url": "https://api.github.com/repos/douglastalbert/demo/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/douglastalbert/demo/merges",
        "archive_url": "https://api.github.com/repos/douglastalbert/demo/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/douglastalbert/demo/downloads",
        "issues_url": "https://api.github.com/repos/douglastalbert/demo/issues{/number}",
        "pulls_url": "https://api.github.com/repos/douglastalbert/demo/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/douglastalbert/demo/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/douglastalbert/demo/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/douglastalbert/demo/labels{/name}",
        "releases_url": "https://api.github.com/repos/douglastalbert/demo/releases{/id}",
        "deployments_url": "https://api.github.com/repos/douglastalbert/demo/deployments",
        "created_at": "2019-06-10T18:40:43Z",
        "updated_at": "2019-06-12T17:23:37Z",
        "pushed_at": "2019-06-20T15:41:02Z",
        "git_url": "git://github.com/douglastalbert/demo.git",
        "ssh_url": "git@github.com:douglastalbert/demo.git",
        "clone_url": "https://github.com/douglastalbert/demo.git",
        "svn_url": "https://github.com/douglastalbert/demo",
        "homepage": None,
        "size": 5,
        "stargazers_count": 0,
        "watchers_count": 0,
        "language": None,
        "has_issues": True,
        "has_projects": True,
        "has_downloads": True,
        "has_wiki": True,
        "has_pages": False,
        "forks_count": 0,
        "mirror_url": None,
        "archived": False,
        "disabled": False,
        "open_issues_count": 0,
        "license": None,
        "forks": 0,
        "open_issues": 0,
        "watchers": 0,
        "default_branch": "master",
        "permissions": {
            "admin": True,
            "push": True,
            "pull": True
        }
    }

    mock_get_repo_patcher = patch("requests.get")
    mock_get_repo = mock_get_repo_patcher.start()
    mock_get_repo.return_value.json.return_value = repo

    r = Repository(MOCK_URL, MOCK_HEADER)
    r.parse_json()
    assert r._id == 191225856
    assert r.name == "demo"
    assert r._pr_url == "https://api.github.com/repos/douglastalbert/demo/pulls?state=all"
    mock_get_repo.stop()

@pytest.mark.skip(reason="Will fail due to unwanted mock calls")
def test_pull_parse_json():
    pr = {
        "url": "https://api.github.com/repos/douglastalbert/demo/pulls/1",
        "id": 287604586,
        "node_id": "MDExOlB1bGxSZXF1ZXN0Mjg3NjA0NTg2",
        "html_url": "https://github.com/douglastalbert/demo/pull/1",
        "diff_url": "https://github.com/douglastalbert/demo/pull/1.diff",
        "patch_url": "https://github.com/douglastalbert/demo/pull/1.patch",
        "issue_url": "https://api.github.com/repos/douglastalbert/demo/issues/1",
        "number": 1,
        "state": "closed",
        "locked": False,
        "title": "Update README.md",
        "user": {
            "login": "douglastalbert",
            "id": 35708020,
            "node_id": "MDQ6VXNlcjM1NzA4MDIw",
            "avatar_url": "https://avatars1.githubusercontent.com/u/35708020?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/douglastalbert",
            "html_url": "https://github.com/douglastalbert",
            "followers_url": "https://api.github.com/users/douglastalbert/followers",
            "following_url": "https://api.github.com/users/douglastalbert/following{/other_user}",
            "gists_url": "https://api.github.com/users/douglastalbert/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/douglastalbert/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/douglastalbert/subscriptions",
            "organizations_url": "https://api.github.com/users/douglastalbert/orgs",
            "repos_url": "https://api.github.com/users/douglastalbert/repos",
            "events_url": "https://api.github.com/users/douglastalbert/events{/privacy}",
            "received_events_url": "https://api.github.com/users/douglastalbert/received_events",
            "type": "User",
            "site_admin": False
        },
        "body": "Example",
        "created_at": "2019-06-12T17:25:10Z",
        "updated_at": "2019-06-20T15:41:02Z",
        "closed_at": "2019-06-20T15:41:02Z",
        "merged_at": "2019-06-20T15:41:02Z",
        "merge_commit_sha": "13737552c56eb8fa3a85b69d94c79e70e9662146",
        "assignee": None,
        "assignees": [],
        "requested_reviewers": [],
        "requested_teams": [],
        "labels": [],
        "milestone": None,
        "commits_url": "https://api.github.com/repos/douglastalbert/demo/pulls/1/commits",
        "review_comments_url": "https://api.github.com/repos/douglastalbert/demo/pulls/1/comments",
        "review_comment_url": "https://api.github.com/repos/douglastalbert/demo/pulls/comments{/number}",
        "comments_url": "https://api.github.com/repos/douglastalbert/demo/issues/1/comments",
        "statuses_url": "https://api.github.com/repos/douglastalbert/demo/statuses/03df5344457820194f4f1440ea33d373eb189765",
        "head": {
            "label": "douglastalbert:master",
            "ref": "master",
            "sha": "03df5344457820194f4f1440ea33d373eb189765",
            "user": {
                "login": "douglastalbert",
                "id": 35708020,
                "node_id": "MDQ6VXNlcjM1NzA4MDIw",
                "avatar_url": "https://avatars1.githubusercontent.com/u/35708020?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/douglastalbert",
                "html_url": "https://github.com/douglastalbert",
                "followers_url": "https://api.github.com/users/douglastalbert/followers",
                "following_url": "https://api.github.com/users/douglastalbert/following{/other_user}",
                "gists_url": "https://api.github.com/users/douglastalbert/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/douglastalbert/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/douglastalbert/subscriptions",
                "organizations_url": "https://api.github.com/users/douglastalbert/orgs",
                "repos_url": "https://api.github.com/users/douglastalbert/repos",
                "events_url": "https://api.github.com/users/douglastalbert/events{/privacy}",
                "received_events_url": "https://api.github.com/users/douglastalbert/received_events",
                "type": "User",
                "site_admin": False
            },
            "repo": {
                "id": 191225856,
                "node_id": "MDEwOlJlcG9zaXRvcnkxOTEyMjU4NTY=",
                "name": "demo",
                "full_name": "douglastalbert/demo",
                "private": False,
                "owner": {
                    "login": "douglastalbert",
                    "id": 35708020,
                    "node_id": "MDQ6VXNlcjM1NzA4MDIw",
                    "avatar_url": "https://avatars1.githubusercontent.com/u/35708020?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/douglastalbert",
                    "html_url": "https://github.com/douglastalbert",
                    "followers_url": "https://api.github.com/users/douglastalbert/followers",
                    "following_url": "https://api.github.com/users/douglastalbert/following{/other_user}",
                    "gists_url": "https://api.github.com/users/douglastalbert/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/douglastalbert/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/douglastalbert/subscriptions",
                    "organizations_url": "https://api.github.com/users/douglastalbert/orgs",
                    "repos_url": "https://api.github.com/users/douglastalbert/repos",
                    "events_url": "https://api.github.com/users/douglastalbert/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/douglastalbert/received_events",
                    "type": "User",
                    "site_admin": False
                },
                "html_url": "https://github.com/douglastalbert/demo",
                "description": "Demo from Udemy git/github course",
                "fork": False,
                "url": "https://api.github.com/repos/douglastalbert/demo",
                "forks_url": "https://api.github.com/repos/douglastalbert/demo/forks",
                "keys_url": "https://api.github.com/repos/douglastalbert/demo/keys{/key_id}",
                "collaborators_url": "https://api.github.com/repos/douglastalbert/demo/collaborators{/collaborator}",
                "teams_url": "https://api.github.com/repos/douglastalbert/demo/teams",
                "hooks_url": "https://api.github.com/repos/douglastalbert/demo/hooks",
                "issue_events_url": "https://api.github.com/repos/douglastalbert/demo/issues/events{/number}",
                "events_url": "https://api.github.com/repos/douglastalbert/demo/events",
                "assignees_url": "https://api.github.com/repos/douglastalbert/demo/assignees{/user}",
                "branches_url": "https://api.github.com/repos/douglastalbert/demo/branches{/branch}",
                "tags_url": "https://api.github.com/repos/douglastalbert/demo/tags",
                "blobs_url": "https://api.github.com/repos/douglastalbert/demo/git/blobs{/sha}",
                "git_tags_url": "https://api.github.com/repos/douglastalbert/demo/git/tags{/sha}",
                "git_refs_url": "https://api.github.com/repos/douglastalbert/demo/git/refs{/sha}",
                "trees_url": "https://api.github.com/repos/douglastalbert/demo/git/trees{/sha}",
                "statuses_url": "https://api.github.com/repos/douglastalbert/demo/statuses/{sha}",
                "languages_url": "https://api.github.com/repos/douglastalbert/demo/languages",
                "stargazers_url": "https://api.github.com/repos/douglastalbert/demo/stargazers",
                "contributors_url": "https://api.github.com/repos/douglastalbert/demo/contributors",
                "subscribers_url": "https://api.github.com/repos/douglastalbert/demo/subscribers",
                "subscription_url": "https://api.github.com/repos/douglastalbert/demo/subscription",
                "commits_url": "https://api.github.com/repos/douglastalbert/demo/commits{/sha}",
                "git_commits_url": "https://api.github.com/repos/douglastalbert/demo/git/commits{/sha}",
                "comments_url": "https://api.github.com/repos/douglastalbert/demo/comments{/number}",
                "issue_comment_url": "https://api.github.com/repos/douglastalbert/demo/issues/comments{/number}",
                "contents_url": "https://api.github.com/repos/douglastalbert/demo/contents/{+path}",
                "compare_url": "https://api.github.com/repos/douglastalbert/demo/compare/{base}...{head}",
                "merges_url": "https://api.github.com/repos/douglastalbert/demo/merges",
                "archive_url": "https://api.github.com/repos/douglastalbert/demo/{archive_format}{/ref}",
                "downloads_url": "https://api.github.com/repos/douglastalbert/demo/downloads",
                "issues_url": "https://api.github.com/repos/douglastalbert/demo/issues{/number}",
                "pulls_url": "https://api.github.com/repos/douglastalbert/demo/pulls{/number}",
                "milestones_url": "https://api.github.com/repos/douglastalbert/demo/milestones{/number}",
                "notifications_url": "https://api.github.com/repos/douglastalbert/demo/notifications{?since,all,participating}",
                "labels_url": "https://api.github.com/repos/douglastalbert/demo/labels{/name}",
                "releases_url": "https://api.github.com/repos/douglastalbert/demo/releases{/id}",
                "deployments_url": "https://api.github.com/repos/douglastalbert/demo/deployments",
                "created_at": "2019-06-10T18:40:43Z",
                "updated_at": "2019-06-12T17:23:37Z",
                "pushed_at": "2019-06-20T15:41:02Z",
                "git_url": "git://github.com/douglastalbert/demo.git",
                "ssh_url": "git@github.com:douglastalbert/demo.git",
                "clone_url": "https://github.com/douglastalbert/demo.git",
                "svn_url": "https://github.com/douglastalbert/demo",
                "homepage": None,
                "size": 5,
                "stargazers_count": 0,
                "watchers_count": 0,
                "language": None,
                "has_issues": True,
                "has_projects": True,
                "has_downloads": True,
                "has_wiki": True,
                "has_pages": False,
                "forks_count": 0,
                "mirror_url": None,
                "archived": False,
                "disabled": False,
                "open_issues_count": 0,
                "license": None,
                "forks": 0,
                "open_issues": 0,
                "watchers": 0,
                "default_branch": "master"
            }
        },
        "base": {
            "label": "douglastalbert:development",
            "ref": "development",
            "sha": "c42be22a8607d99ef2011064039aea2359eac246",
            "user": {
                "login": "douglastalbert",
                "id": 35708020,
                "node_id": "MDQ6VXNlcjM1NzA4MDIw",
                "avatar_url": "https://avatars1.githubusercontent.com/u/35708020?v=4",
                "gravatar_id": "",
                "url": "https://api.github.com/users/douglastalbert",
                "html_url": "https://github.com/douglastalbert",
                "followers_url": "https://api.github.com/users/douglastalbert/followers",
                "following_url": "https://api.github.com/users/douglastalbert/following{/other_user}",
                "gists_url": "https://api.github.com/users/douglastalbert/gists{/gist_id}",
                "starred_url": "https://api.github.com/users/douglastalbert/starred{/owner}{/repo}",
                "subscriptions_url": "https://api.github.com/users/douglastalbert/subscriptions",
                "organizations_url": "https://api.github.com/users/douglastalbert/orgs",
                "repos_url": "https://api.github.com/users/douglastalbert/repos",
                "events_url": "https://api.github.com/users/douglastalbert/events{/privacy}",
                "received_events_url": "https://api.github.com/users/douglastalbert/received_events",
                "type": "User",
                "site_admin": False
            },
            "repo": {
                "id": 191225856,
                "node_id": "MDEwOlJlcG9zaXRvcnkxOTEyMjU4NTY=",
                "name": "demo",
                "full_name": "douglastalbert/demo",
                "private": False,
                "owner": {
                    "login": "douglastalbert",
                    "id": 35708020,
                    "node_id": "MDQ6VXNlcjM1NzA4MDIw",
                    "avatar_url": "https://avatars1.githubusercontent.com/u/35708020?v=4",
                    "gravatar_id": "",
                    "url": "https://api.github.com/users/douglastalbert",
                    "html_url": "https://github.com/douglastalbert",
                    "followers_url": "https://api.github.com/users/douglastalbert/followers",
                    "following_url": "https://api.github.com/users/douglastalbert/following{/other_user}",
                    "gists_url": "https://api.github.com/users/douglastalbert/gists{/gist_id}",
                    "starred_url": "https://api.github.com/users/douglastalbert/starred{/owner}{/repo}",
                    "subscriptions_url": "https://api.github.com/users/douglastalbert/subscriptions",
                    "organizations_url": "https://api.github.com/users/douglastalbert/orgs",
                    "repos_url": "https://api.github.com/users/douglastalbert/repos",
                    "events_url": "https://api.github.com/users/douglastalbert/events{/privacy}",
                    "received_events_url": "https://api.github.com/users/douglastalbert/received_events",
                    "type": "User",
                    "site_admin": False
                },
                "html_url": "https://github.com/douglastalbert/demo",
                "description": "Demo from Udemy git/github course",
                "fork": False,
                "url": "https://api.github.com/repos/douglastalbert/demo",
                "forks_url": "https://api.github.com/repos/douglastalbert/demo/forks",
                "keys_url": "https://api.github.com/repos/douglastalbert/demo/keys{/key_id}",
                "collaborators_url": "https://api.github.com/repos/douglastalbert/demo/collaborators{/collaborator}",
                "teams_url": "https://api.github.com/repos/douglastalbert/demo/teams",
                "hooks_url": "https://api.github.com/repos/douglastalbert/demo/hooks",
                "issue_events_url": "https://api.github.com/repos/douglastalbert/demo/issues/events{/number}",
                "events_url": "https://api.github.com/repos/douglastalbert/demo/events",
                "assignees_url": "https://api.github.com/repos/douglastalbert/demo/assignees{/user}",
                "branches_url": "https://api.github.com/repos/douglastalbert/demo/branches{/branch}",
                "tags_url": "https://api.github.com/repos/douglastalbert/demo/tags",
                "blobs_url": "https://api.github.com/repos/douglastalbert/demo/git/blobs{/sha}",
                "git_tags_url": "https://api.github.com/repos/douglastalbert/demo/git/tags{/sha}",
                "git_refs_url": "https://api.github.com/repos/douglastalbert/demo/git/refs{/sha}",
                "trees_url": "https://api.github.com/repos/douglastalbert/demo/git/trees{/sha}",
                "statuses_url": "https://api.github.com/repos/douglastalbert/demo/statuses/{sha}",
                "languages_url": "https://api.github.com/repos/douglastalbert/demo/languages",
                "stargazers_url": "https://api.github.com/repos/douglastalbert/demo/stargazers",
                "contributors_url": "https://api.github.com/repos/douglastalbert/demo/contributors",
                "subscribers_url": "https://api.github.com/repos/douglastalbert/demo/subscribers",
                "subscription_url": "https://api.github.com/repos/douglastalbert/demo/subscription",
                "commits_url": "https://api.github.com/repos/douglastalbert/demo/commits{/sha}",
                "git_commits_url": "https://api.github.com/repos/douglastalbert/demo/git/commits{/sha}",
                "comments_url": "https://api.github.com/repos/douglastalbert/demo/comments{/number}",
                "issue_comment_url": "https://api.github.com/repos/douglastalbert/demo/issues/comments{/number}",
                "contents_url": "https://api.github.com/repos/douglastalbert/demo/contents/{+path}",
                "compare_url": "https://api.github.com/repos/douglastalbert/demo/compare/{base}...{head}",
                "merges_url": "https://api.github.com/repos/douglastalbert/demo/merges",
                "archive_url": "https://api.github.com/repos/douglastalbert/demo/{archive_format}{/ref}",
                "downloads_url": "https://api.github.com/repos/douglastalbert/demo/downloads",
                "issues_url": "https://api.github.com/repos/douglastalbert/demo/issues{/number}",
                "pulls_url": "https://api.github.com/repos/douglastalbert/demo/pulls{/number}",
                "milestones_url": "https://api.github.com/repos/douglastalbert/demo/milestones{/number}",
                "notifications_url": "https://api.github.com/repos/douglastalbert/demo/notifications{?since,all,participating}",
                "labels_url": "https://api.github.com/repos/douglastalbert/demo/labels{/name}",
                "releases_url": "https://api.github.com/repos/douglastalbert/demo/releases{/id}",
                "deployments_url": "https://api.github.com/repos/douglastalbert/demo/deployments",
                "created_at": "2019-06-10T18:40:43Z",
                "updated_at": "2019-06-12T17:23:37Z",
                "pushed_at": "2019-06-20T15:41:02Z",
                "git_url": "git://github.com/douglastalbert/demo.git",
                "ssh_url": "git@github.com:douglastalbert/demo.git",
                "clone_url": "https://github.com/douglastalbert/demo.git",
                "svn_url": "https://github.com/douglastalbert/demo",
                "homepage": None,
                "size": 5,
                "stargazers_count": 0,
                "watchers_count": 0,
                "language": None,
                "has_issues": True,
                "has_projects": True,
                "has_downloads": True,
                "has_wiki": True,
                "has_pages": False,
                "forks_count": 0,
                "mirror_url": None,
                "archived": False,
                "disabled": False,
                "open_issues_count": 0,
                "license": None,
                "forks": 0,
                "open_issues": 0,
                "watchers": 0,
                "default_branch": "master"
            }
        },
        "_links": {
            "self": {
                "href": "https://api.github.com/repos/douglastalbert/demo/pulls/1"
            },
            "html": {
                "href": "https://github.com/douglastalbert/demo/pull/1"
            },
            "issue": {
                "href": "https://api.github.com/repos/douglastalbert/demo/issues/1"
            },
            "comments": {
                "href": "https://api.github.com/repos/douglastalbert/demo/issues/1/comments"
            },
            "review_comments": {
                "href": "https://api.github.com/repos/douglastalbert/demo/pulls/1/comments"
            },
            "review_comment": {
                "href": "https://api.github.com/repos/douglastalbert/demo/pulls/comments{/number}"
            },
            "commits": {
                "href": "https://api.github.com/repos/douglastalbert/demo/pulls/1/commits"
            },
            "statuses": {
                "href": "https://api.github.com/repos/douglastalbert/demo/statuses/03df5344457820194f4f1440ea33d373eb189765"
            }
        },
        "author_association": "OWNER",
        "merged": True,
        "mergeable": None,
        "rebaseable": None,
        "mergeable_state": "unknown",
        "merged_by": {
            "login": "douglastalbert",
            "id": 35708020,
            "node_id": "MDQ6VXNlcjM1NzA4MDIw",
            "avatar_url": "https://avatars1.githubusercontent.com/u/35708020?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/douglastalbert",
            "html_url": "https://github.com/douglastalbert",
            "followers_url": "https://api.github.com/users/douglastalbert/followers",
            "following_url": "https://api.github.com/users/douglastalbert/following{/other_user}",
            "gists_url": "https://api.github.com/users/douglastalbert/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/douglastalbert/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/douglastalbert/subscriptions",
            "organizations_url": "https://api.github.com/users/douglastalbert/orgs",
            "repos_url": "https://api.github.com/users/douglastalbert/repos",
            "events_url": "https://api.github.com/users/douglastalbert/events{/privacy}",
            "received_events_url": "https://api.github.com/users/douglastalbert/received_events",
            "type": "User",
            "site_admin": False
        },
        "comments": 0,
        "review_comments": 0,
        "maintainer_can_modify": False,
        "commits": 1,
        "additions": 1,
        "deletions": 0,
        "changed_files": 1
    }
    mock_get_pr_patcher = patch("requests.get")
    mock_get_pr = mock_get_pr_patcher.start()
    mock_get_pr.return_value.json.return_value = pr

    pull = PullRequest(MOCK_URL, MOCK_HEADER)
    pull.parse_json()
    ##Fails because mock_get_pr always returns pr json
    ##so unable to initialize Repository
    assert str(pull) == "State: closed, User: douglastalbert"
    assert pull.changed_files == 1
    mock_get_pr.stop()
