from flask import Flask, render_template, send_from_directory
import requests
import os

app = Flask(__name__)

# GitHub Username and Resume Info
GITHUB_USERNAME = 'vignesh8682091237'
RESUME_REPO = 'vignesh8682091237'  # Use the repository name containing your resume
RESUME_FILENAME = 'resume.pdf'

# 🔽 Get GitHub Projects from API
def get_github_projects(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        projects = []
        for repo in repos:
            projects.append({
                'name': repo['name'],
                'description': repo['description'] or 'No description provided.',
                'html_url': repo['html_url'],
                'homepage': repo['homepage'] or '',
            })
        return projects
    else:
        return []

# 🔽 Get Certificate Images from static/certificates/
def get_certificates():
    cert_folder = os.path.join('static', 'certificates')
    certificate_files = [
        f for f in os.listdir(cert_folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg'))
    ]
    certificate_files.sort()
    return certificate_files

# 🔽 Download Latest Resume PDF from GitHub
def update_resume_pdf(username, repo, filename):
    resume_url = f'https://raw.githubusercontent.com/{username}/{repo}/main/{filename}'
    resume_folder = os.path.join('static', 'resume')
    os.makedirs(resume_folder, exist_ok=True)
    file_path = os.path.join(resume_folder, filename)

    try:
        response = requests.get(resume_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
    except Exception as e:
        print(f"Error updating resume: {e}")

# 🔽 Home Page
@app.route('/')
def home():
    projects = get_github_projects(GITHUB_USERNAME)
    certificates = get_certificates()
    update_resume_pdf(GITHUB_USERNAME, RESUME_REPO, RESUME_FILENAME)
    return render_template('home.html', projects=projects, certificates=certificates)

# 🔽 Resume Download/View Route
@app.route('/resume')
def resume():
    return send_from_directory('static/resume', RESUME_FILENAME)

# 🔽 Run App
if __name__ == '__main__':
    app.run(debug=True)
