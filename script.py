import requests
import json
import time
import argparse
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def remove_collaborator(repo_owner, repo_name, collaborator_username, github_token):
    """Removes a collaborator from a GitHub repository."""

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators/{collaborator_username}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print(f"Successfully removed {collaborator_username} from {repo_owner}/{repo_name}")
    elif response.status_code == 404:
        print(
            f"Error: {collaborator_username} is not a collaborator on {repo_owner}/{repo_name}"
        )
    else:
        print(
            f"Error removing {collaborator_username}. Status code: {response.status_code}"
        )
        print(response.text)


def get_collaborator_repos(repo_owner, repo_name, collaborator_username, github_token):
    """Checks if a user is a collaborator on a GitHub repository and lists them."""

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators/{collaborator_username}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 204 or response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        print(
            f"Error checking {collaborator_username} on {repo_owner}/{repo_name}. Status code: {response.status_code}"
        )
        print(response.text)
        return False


def get_all_organizations(github_token):
    """Fetches all organizations for a user."""

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    url = "https://api.github.com/user/orgs"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        organizations = response.json()
        print(f"Found {len(organizations)} organizations")
        return organizations
    else:
        print(f"Error getting organizations. Status code: {response.status_code}")
        print(response.text)
        return []


def handle_rate_limit(response):
    """Checks for rate limit headers and adds a delay if needed."""
    if "X-RateLimit-Remaining" in response.headers:
        remaining = int(response.headers["X-RateLimit-Remaining"])
        print(f"API Remaining Requests: {remaining}")
        if remaining < 10:
            reset_time = int(response.headers["X-RateLimit-Reset"])
            wait_time = reset_time - int(time.time()) + 5  # Add some grace
            if wait_time > 0:
                print(f"Rate limit is low, waiting {wait_time} seconds...")
                time.sleep(wait_time)


if __name__ == "__main__":
    # Setup Argument Parser
    parser = argparse.ArgumentParser(
        description="Check or remove GitHub collaborator across all organizations and repositories.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
        Usage Examples:
          
          To list repositories where a user is a collaborator:
            python script.py <USERNAME>

          To remove a collaborator from all repos with user confirmation:
            python script.py <USERNAME> --delete

          To forcefully remove a collaborator without user confirmation:
            python script.py <USERNAME> --deleteforcefull
        """,
    )
    parser.add_argument(
        "collaborator_username", help="The GitHub username to check or remove"
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Include this flag to delete the collaborator with user confirmation. Otherwise, just list repositories.",
    )
    parser.add_argument(
        "--deleteforcefull",
        action="store_true",
        help="Include this flag to delete the collaborator without user confirmation from all the repos.\nWARNING: Use with extreme caution.",
    )
    args = parser.parse_args()

    # Get the GitHub token from environment variables
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        exit(1)

    collaborator_username = args.collaborator_username
    delete_collaborator = args.delete
    delete_forcefull = args.deleteforcefull

    all_orgs = get_all_organizations(github_token)

    if not all_orgs:
        print("No organizations found, exiting.")
        exit()

    print(f"Checking for user '{collaborator_username}' in repositories...")

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    user_found = False
    for org in all_orgs:
        org_name = org["login"]

        repos_url = f"https://api.github.com/orgs/{org_name}/repos"
        repos_response = requests.get(repos_url, headers=headers)
        handle_rate_limit(repos_response)

        if repos_response.status_code == 200:
            repos = repos_response.json()
            for repo in repos:
                repo_name = repo["name"]
                is_collaborator = get_collaborator_repos(
                    org_name, repo_name, collaborator_username, github_token
                )
                if is_collaborator:
                    print(
                        f"User '{collaborator_username}' is a collaborator in: {org_name}/{repo_name}"
                    )
                    user_found = True
                    if delete_forcefull:
                        remove_collaborator(
                            org_name,
                            repo_name,
                            collaborator_username,
                            github_token,
                        )
                    elif delete_collaborator:
                        confirm = input(
                            f"Are you sure you want to remove '{collaborator_username}' from {org_name}/{repo_name}? (y/n): "
                        )
                        if confirm.lower() == "y":
                            remove_collaborator(
                                org_name,
                                repo_name,
                                collaborator_username,
                                github_token,
                            )
                        else:
                            print(f"Skipping removal from {org_name}/{repo_name}")
        else:
            print(
                f"Error getting repos for organization: {org_name}. Status code: {repos_response.status_code}"
            )
            print(repos_response.text)

    if not user_found:
        print(f"User '{collaborator_username}' not found in any repository.")

    print("Script finished.")