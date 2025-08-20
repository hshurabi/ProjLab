import os
from dotenv import load_dotenv
from pathlib import Path
import questionary
from github import Github
import shutil
import subprocess
from urllib.parse import urlparse

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_PAT_TOKEN = os.getenv("GITHUB_PAT_TOKEN")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if not GITHUB_PAT_TOKEN:
        raise RuntimeError("GITHUB_PAT_TOKEN missing. Did you load the correct .env?")


def create_structure(project_name, project_type):
    project_path = PROJECT_ROOT / project_type / project_name
    project_path.mkdir(parents=True, exist_ok=True)

    # Common folders
    os.makedirs(os.path.join(project_path, "data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "results"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "notebooks"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "related-files"), exist_ok=True)

    # Copy sample data and notebook template
    templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    source_file = os.path.join(templates_path, "get_started.ipynb")
    dest_file = os.path.join(project_path, "notebooks", "get_started.ipynb")

    shutil.copy(source_file, dest_file)
    # Repo setup (optional, done later)
    return project_path

def create_github_repo(repo_name):
    g = Github(GITHUB_PAT_TOKEN)
    user = g.get_user()
    print(user)
    try:
        repo = user.get_repo(repo_name)
        print(f"⚠️ Repo '{repo_name}' already exists. Using existing repo.")
    except:
        # Repo doesn't exist; safe to create
        repo = user.create_repo(repo_name)
        print(f"✅ Created new repo '{repo_name}'")
    return repo.clone_url

def create_conda_env(env_name, project_path):
    print(f"\n📦 Creating Conda environment: {env_name}")
    os.system(f'conda create -y -n {env_name} python=3.11')
    
    env_yml = project_path / "environment.yml"
    with open(env_yml, "w") as f:
        f.write(f"name: {env_name}\ndependencies:\n  - python=3.11\n")

    print(f"\n✅ Environment created. To activate it:")
    print(f"   conda activate {env_name}")

    print(f"\n📄 A starter environment.yml was added at: {env_yml}")


def initialize_git_repo(path, remote_url):
    os.chdir(path)
    os.system("git init")
    os.system("git add .")
    os.system('git commit -m "Initial commit"')
    os.system(f"git remote add origin {remote_url}")
    os.system("git branch -M main")
    os.system("git push -u origin main")

def parse_github_https_url(url: str):
    """
    Parse a GitHub HTTPS repo URL and return (owner, repo_name).

    Examples:
        https://github.com/owner/repo.git  -> ("owner", "repo")
        https://github.com/org/project     -> ("org", "project")
    """
    # First strip trailing ".git" if present
    if url.endswith(".git"):
        url = url[:-4]

    # Validate and parse
    parsed = urlparse(url)
    if parsed.netloc not in ("github.com", "www.github.com"):
        raise ValueError(f"Not a valid GitHub HTTPS URL: {url}")

    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) != 2:
        raise ValueError(f"Unexpected GitHub path format: {parsed.path}")

    owner, repo = path_parts
    return owner, repo

def clone_and_setup_repo(repo_url, target_path, env_name, fallback_path):
    """
    owner: 'your-user-or-org'
    repo_name: 'my-repo'
    target_path: path where the repo folder should be created (must not exist)
    """
    owner, repo_name = parse_github_https_url(repo_url)
    # SSH via your alias (best for multi-account)
    ssh_host = os.getenv("SSH_HOST")  # e.g., github-biz or github-personal
    if not ssh_host:
        print("SSH_HOST not set in env; trying with HTTPS ...")
        # HTTPS (uses Git Credential Manager to prompt/cache PAT)
        remote_url = f"https://github.com/{owner}/{repo_name}.git"
    else:
        remote_url = f"git@{ssh_host}:{owner}/{repo_name}.git"
        
    try:
        subprocess.run(["git", "clone", remote_url, str(target_path)], check=True)
        print(f"✅ Repo cloned to {target_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to clone the repo: {e}")
        return

    env_yml_path = os.path.join(target_path, "environment.yml")
    handle_env_creation(env_yml_path, env_name, fallback_path)


def handle_env_creation(env_yml_path, env_name, fallback_path):
    if os.path.exists(env_yml_path):
        if questionary.confirm("An environment.yml file was found. Create environment from this file?").ask():
            os.system(f"conda env create -f {env_yml_path} -n {env_name}")
            print(f"✅ Environment '{env_name}' created from YAML")
        elif questionary.confirm("Do you want to create a new environment manually?").ask():
            create_conda_env(env_name, fallback_path)
    else:
        if questionary.confirm("Do you want to create a new Conda environment for this project?").ask():
            env_name = questionary.text("Environment name:", default=env_name).ask()
            create_conda_env(env_name, fallback_path)


def main():
    project_name = questionary.text("Project name:").ask()
    project_type = questionary.select("Project type:", choices=["tmp", "poc", "prod"]).ask()

    project_path = create_structure(project_name, project_type)
    repo_subdir = os.path.join(project_path, "repo")

    has_repo = questionary.confirm("Do you already have a GitHub repo for this project?").ask()

    if has_repo:
        repo_url = questionary.text("Enter the GitHub repo URL:").ask()
        clone_and_setup_repo(repo_url, repo_subdir, project_name, project_path)
    else:
        if questionary.confirm("Do you want to create a new GitHub repo?").ask():
            repo_url = create_github_repo(project_name)
            initialize_git_repo(project_path, repo_url)
            clone_and_setup_repo(repo_url, repo_subdir, project_name, project_path)
        else:
            # If no GitHub repo at all, still optionally create env
            if questionary.confirm("Do you want to create a new Conda environment for this project?").ask():
                env_name = questionary.text("Environment name:", default=project_name).ask()
                create_conda_env(env_name, project_path)

    print(f"\n✅ Project '{project_name}' is ready at: {project_path}")


if __name__ == "__main__":
    main()
