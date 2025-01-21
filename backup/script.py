import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_collaborator_repos(repo_owner, repo_name, collaborator_username, github_token):
    """Checks if a user is a collaborator on a GitHub repository and lists them."""
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators/{collaborator_username}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 204 or response.status_code == 200:
        return True
    elif response.status_code == 404:
        return False
    else:
        print(f"Error checking {collaborator_username} on {repo_owner}/{repo_name}. Status code: {response.status_code}")
        print(response.text)
        return False

def get_all_organizations(github_token):
    """Fetches all organizations for a user."""
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
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
    # Get the GitHub token from environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is not set.")
        exit(1)

    collaborator_username = "abdulmalikKryptoMind"  # Replace with the GitHub username to check

    all_orgs = get_all_organizations(github_token)
    
    if not all_orgs:
        print("No organizations found, exiting.")
        exit()
      
    print(f"Checking for user '{collaborator_username}' in repositories...")
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    for org in all_orgs:
        org_name = org['login']
        
        repos_url = f"https://api.github.com/orgs/{org_name}/repos"
        repos_response = requests.get(repos_url, headers=headers)
        handle_rate_limit(repos_response)

        if repos_response.status_code == 200:
            repos = repos_response.json()
            for repo in repos:
                repo_name = repo['name']
                is_collaborator = get_collaborator_repos(org_name, repo_name, collaborator_username, github_token)
                if is_collaborator:
                    print(f"User '{collaborator_username}' is a collaborator in: {org_name}/{repo_name}")
        else:
            print(f"Error getting repos for organization: {org_name}. Status code: {repos_response.status_code}")
            print(repos_response.text)
