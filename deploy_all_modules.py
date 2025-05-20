"""Script to trigger GitHub actions to deploy all modules.

Triggers:

- Deploy to SWOT-Confluence AWS
"""

# Standard imports
import argparse
import logging

# Third-party imports
import requests


logging.getLogger(name="trigger_github_actions").setLevel(logging.INFO)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%dT%H:%M:%S',
                    level=logging.INFO)


# Constants
OWNER = "SWOT-Confluence"
TOP_LEVEL_ACTIONS = [
    "VPC Network",
    "Infrastructure"
]
REPO_LIST = [
    "clean_up",
    "combine_data",
    "init_workflow",
    "input",
    "Lakeflow_Confluence",
    "metroman",
    "metroman_consolidation",
    "moi",
    "momma",
    "neobam",
    "offline-discharge-data-product-creation",
    "output",
    "postdiagnostics",
    "prediagnostics",
    "priors",
    "report",
    "sad",
    "setfinder",
    "sic4dvar",
    "validation",
    "ssc_model_deployment",
    "ssc_input"
]


def trigger_github_actions():

    arg_parser = create_args()
    args = arg_parser.parse_args()
    token = args.ghtoken
    branch = args.branch
    version = args.version
    venue = args.venue
    top_level = args.toplevel

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    if top_level:
        deploy_top_level(headers, branch, version, venue)

    deploy_all_modules(headers, branch, version, venue)

    if top_level:
        deploy_step_function(headers, branch, version, venue)

def create_args():
    """Create and return argparser with arguments."""
    arg_parser = argparse.ArgumentParser(description="Retrieve a list of S3 URIs")
    arg_parser.add_argument("-t",
                            "--ghtoken",
                            type=str,
                            help="GitHub token to perform API requests")
    arg_parser.add_argument("-b",
                            "--branch",
                            type=str,
                            help="Branch to deploy")
    arg_parser.add_argument("-n",
                            "--venue",
                            type=str,
                            help="Venue to deploy to")
    arg_parser.add_argument("-v",
                            "--version",
                            type=str,
                            help="Version to deploy under")
    arg_parser.add_argument("-a",
                            "--toplevel",
                            help="Indicate should deploy top-level Terraform",
                            action="store_true")
    return arg_parser

def deploy_top_level(headers, branch, version, venue):
    """Deploy top-level Confluence infrastructure."""

    for action in TOP_LEVEL_ACTIONS:
        logging.info(f"confluence-terraform {action}")
        url = f"https://api.github.com/repos/{OWNER}/confluence-terraform/actions/workflows/deploy.yml/dispatches"
        json_body = {
            "ref": branch,
            "inputs": {
                "venue": venue,
                "deployment": action,
                "version": version
            }
        }
        make_request(url, headers, json_body)

def deploy_all_modules(headers, branch, version, venue):
    """Deploy all repo modules."""

    for repo in REPO_LIST:
        logging.info(repo)
        url = f"https://api.github.com/repos/{OWNER}/{repo}/actions/workflows/deploy.yml/dispatches"
        json_body = {
            "ref": branch,
            "inputs": {
                "venue": venue,
                "version": version
            }
        }
        make_request(url, headers, json_body)

def deploy_step_function(headers, branch, version, venue):
    """Deploy top-level Confluence infrastructure."""

    logging.info("confluence-sfn")
    url = f"https://api.github.com/repos/{OWNER}/confluence-terraform/actions/workflows/deploy.yml/dispatches"
    json_body = {
        "ref": branch,
        "inputs": {
            "venue": venue,
            "deployment": "Step Function",
            "version": version
        }
    }
    make_request(url, headers, json_body)

def make_request(url, headers, json_body):
    """Send a request to the GH Action API."""
    r = requests.post(url, headers=headers, json=json_body)
    try:
        logging.info(r.json())
    except:
        logging.info(r)

if __name__ == "__main__":
    trigger_github_actions()
