"""Script to trigger GitHub actions to create a release for all modules.

Triggers:

- Release creation
- Build of Docker container image
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
CONTAINER_LIST = [
    "clean_up",
    "combine_data",
    "init_workflow",
    "input",
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
RELEASE_LIST = CONTAINER_LIST + ["confluence-terraform"]


def trigger_github_actions():

    arg_parser = create_args()
    args = arg_parser.parse_args()
    token = args.token
    branch = args.branch
    version = args.version

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    build_containers(headers, branch, version)

    tag_release(headers, branch, version)

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
    arg_parser.add_argument("-v",
                            "--version",
                            type=str,
                            help="Version to deploy under")
    return arg_parser

def build_containers(headers, branch, version):
    """Deploy top-level Confluence infrastructure."""

    logging.info("build containers")
    for repo in CONTAINER_LIST:
        logging.info(repo)
        url = f"https://api.github.com/repos/{OWNER}/{repo}/actions/workflows/container.yml/dispatches"
        json_body = {
            "ref": branch,
            "inputs": {
                "version": version
            }
        }
        make_request(url, headers, json_body)

def tag_release(headers, branch, version):
    """Deploy top-level Confluence infrastructure."""

    logging.info("tag release")
    for repo in RELEASE_LIST:
        logging.info(repo)
        url = f"https://api.github.com/repos/{OWNER}/{repo}/actions/workflows/release.yml/dispatches"
        json_body = {
            "ref": branch,
            "inputs": {
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
