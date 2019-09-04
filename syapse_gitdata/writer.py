import csv
from syapse_gitdata.pull import PullRequest
from syapse_gitdata.api_accessor import Accessor
from syapse_gitdata.repository import Repository
from syapse_gitdata.structlogger import structlog
import json
import sys

LOG = structlog.get_logger()

def write_csv(prs) -> None:
    """Writes a csv file using data from the PullRequests provided."""
    LOG.info("Attempting to write to output.csv...")
    with open('syapse_gitdata/output.csv', mode='w') as file_out:
        LOG.info("Successfully accessed output.csv")
        file_writer = csv.writer(file_out, delimiter=',')
        file_writer.writerow(['repo','user','state','url','created', \
                            'updated','closed','assignees','reviewers', \
                            'review_teams','labels','branch','merged', \
                            'comments','review_comments','commits', \
                            'additions','deletions','changed_files'])
        for pr in prs:
            file_writer.writerow(pr.csv_format())

def write_json(prs) -> None:
    """Writes a json file using data from the PullRequests provided."""
    LOG.info("Attempting to write to output.json...")
    pr_list = []
    LOG.info("Converting pull request objects...")
    for pr in prs:
        pr_dict = pr.json_format()
        pr_list.append(pr_dict)
    with open('syapse_gitdata/output.json', 'w') as file_out:
        json.dump(pr_list, file_out)
        LOG.info("Successfully accessed output.json")

def update_json(prs) -> None:
    """Takes a list of new/updated prs and writes them to output.json"""
    with open('syapse_gitdata/output.json', 'r') as file_out:
        # for line in file_out:
        #     print(line)
        prs_in_file = json.load(file_out)
        LOG.info('File Loaded Successfully')
        in_file_dict = {}
        for pr in prs_in_file:
            in_file_dict.update({pr['url'] : pr})
        for pr in prs:
            # pr_dict = pr.json_format()
            if pr.url in in_file_dict.keys():
                in_file_dict['url'] = pr.json_format()
            else:
                in_file_dict.update({pr.url : pr.json_format()})
    with open('syapse_gitdata/output.json', 'w') as file_out:
        json.dump(list(in_file_dict.values()), file_out)
    LOG.info("Successfully accessed output.json")
