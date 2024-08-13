import os
import argparse
import json
from datetime import datetime
import logging
from collections import defaultdict
from dateutil.relativedelta import relativedelta
import requests


ARTIFACTORY_URL = 'https://artifactory.example.com/artifactory'
API_ENDPOINT = f'{ARTIFACTORY_URL}/api/search/aql'
USERNAME = os.environ['ARTIFACTORY_USERNAME']
PASSWORD = os.environ['ARTIFACTORY_PASSWORD']
CURRENT_TIME = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
LOG_FILE = f'cleanup_docker_images_{CURRENT_TIME}.log'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler(LOG_FILE),
                    ])
logger = logging.getLogger(__name__)


def get_date_offset(date_string):
    num = int(date_string[:-1])
    period = date_string[-1]

    current_date = datetime.utcnow()
    if period == 'm':
        return current_date - relativedelta(months=num)
    elif period == 'y':
        return current_date - relativedelta(years=num)
    else:
        raise ValueError(
            "Unsupported time period. Use 'm' for months or 'y' for years.")


def build_aql_query(repo_name, created):
    created_date = get_date_offset(created).strftime('%Y-%m-%dT%H:%M:%S.000Z')

    query = f'''
items.find({{
    "repo": "{repo_name}",
    "created": {{"$lt": "{created_date}"}},
    "name": {{"$match": "manifest.json"}},
    "path": {{"$nmatch": "*latest*"}}
}}).include("name", "repo", "path", "created")
    '''

    return query


def delete_artifact(delete_url, dry_run):
    if dry_run:
        logger.info(
            f"[DRY RUN] Will be deleted: {delete_url}\n----------------------------------")
    else:
        response = requests.delete(delete_url, auth=(USERNAME, PASSWORD))
        if response.status_code == 204:
            logger.info(
                f"Deleted: {delete_url}\n----------------------------------")
        else:
            logger.error(
                f"Failed to delete {delete_url}: {response.status_code} - {response.text}")


def main(repo_name, created, dry_run):
    aql_query = build_aql_query(repo_name, created)

    headers = {"Content-Type": "text/plain"}
    response = requests.post(API_ENDPOINT, auth=(
        USERNAME, PASSWORD), data=aql_query, headers=headers)

    if response.status_code == 200:
        results = response.json()
        grouped_items = defaultdict(list)
        for item in results['results']:
            parent_directory = '/'.join(item['path'].split('/')[:-1])
            grouped_items[parent_directory].append(item)

        for parent_directory, items in grouped_items.items():
            sorted_items = sorted(
                items, key=lambda x: x['created'], reverse=True)

            items_to_delete = sorted_items[5:]
            for item in items_to_delete:
                repo = item['repo']
                path = item['path']
                logger.info(json.dumps(item, indent=4))
                delete_url = f"{ARTIFACTORY_URL}/{repo}/{path}"
                delete_artifact(delete_url, dry_run)
    else:
        logger.error(
            f"Failed to fetch artifacts: {response.status_code} - {response.text}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Artifactory AQL query script.')
    parser.add_argument('--repo-name', required=True,
                        help='The name of the repository.')
    parser.add_argument('--created', required=True,
                        help='Find artifacts created before the specified date (e.g., 3m for 3 months ago).')
    parser.add_argument('--dry-run', action='store_true',
                        help='Perform a dry run without actually deleting any artifacts.')

    args = parser.parse_args()

    main(args.repo_name, args.created, args.dry_run)
