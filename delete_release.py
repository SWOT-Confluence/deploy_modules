"""Script to trigger GitHub actions to delete a release for all modules.

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
RELEASE_LIST = [
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
    "ssc_input",
    "confluence-terraform"
]

def github_requests():

    arg_parser = create_args()
    args = arg_parser.parse_args()
    token = args.ghtoken
    version = args.version

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }


    for repo in RELEASE_LIST:
        logging.info("delete release")
        delete_release(repo, headers, version)

        logging.info("delete tag")
        delete_tag(repo, headers, version)

def create_args():
    """Create and return argparser with arguments."""
    arg_parser = argparse.ArgumentParser(description="Retrieve a list of S3 URIs")
    arg_parser.add_argument("-t",
                            "--ghtoken",
                            type=str,
                            help="GitHub token to perform API requests")
    arg_parser.add_argument("-v",
                            "--version",
                            type=str,
                            help="Version to deploy under")
    return arg_parser

def delete_release(repo, headers, version):
    """Deploy top-level Confluence infrastructure."""

    # locate release id
    url = f"https://api.github.com/repos/{OWNER}/{repo}/releases/tags/{version}"
    r = requests.get(url, headers=headers)
    release_id = r.json()["id"]

    # delete release
    url = f"https://api.github.com/repos/{OWNER}/{repo}/releases/{release_id}"
    logging.info("%s: %s", repo, url)
    r = requests.delete(url, headers=headers)
    logging.info(r)

def delete_tag(repo, headers, version):
    """Deploy top-level Confluence infrastructure."""

    # delete tag
    url = f"https://api.github.com/repos/{OWNER}/{repo}/git/refs/tags/{version}"
    logging.info("%s: %s", repo, url)
    r = requests.delete(url, headers=headers)
    logging.info(r)

if __name__ == "__main__":
    github_requests()
