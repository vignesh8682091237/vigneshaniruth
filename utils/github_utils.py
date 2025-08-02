import requests

def get_github_projects(username):
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url)
        response.raise_for_status()  # raises error for bad status
        repos = response.json()
        projects = []

        for repo in repos:
            projects.append({
                'name': repo['name'],
                'description': repo['description'] or 'No description provided',
                'url': repo['html_url']
            })

        return projects
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch GitHub repos: {e}")
        return []
import requests

def get_github_projects(username):
    url = f"https://api.github.com/users/{username}/repos"
    try:
        response = requests.get(url)
        response.raise_for_status()  # raises error for bad status
        repos = response.json()
        projects = []

        for repo in repos:
            projects.append({
                'name': repo['name'],
                'description': repo['description'] or 'No description provided',
                'url': repo['html_url']
            })

        return projects
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch GitHub repos: {e}")
        return []
