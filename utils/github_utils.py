import requests
import os

def get_github_projects(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    repos = []

    if response.status_code == 200:
        for repo in response.json():
            repos.append({
                'name': repo['name'],
                'description': repo['description'],
                'html_url': repo['html_url']
            })
    else:
        print("GitHub API error:", response.status_code)
    return repos

def update_resume_pdf(username, repo_name, file_name):
    url = f'https://raw.githubusercontent.com/{username}/{repo_name}/main/{file_name}'
    local_path = os.path.join('static', 'resume', file_name)

    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    response = requests.get(url)

    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)
    else:
        print("Resume download failed:", response.status_code)
