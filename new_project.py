import os
from pathlib import Path
import questionary
from github import Github
import shutil
import subprocess

def load_github_token_from_readme():
    projects_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # one level up
    readme_path = os.path.join(projects_root, "README.txt")

    if not os.path.exists(readme_path):
        raise FileNotFoundError(f"README.txt not found in {projects_root}")

    with open(readme_path, "r") as f:
        for line in f:
            if "Current Github PAT:" in line:
                token = line.strip().split("Current Github PAT:")[1].strip().split()[0]
                return token

    raise ValueError("GitHub token not found in README.txt")

# Set your GitHub username and token
GITHUB_USERNAME = "hshurabi"
GITHUB_TOKEN = load_github_token_from_readme()

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def create_structure(project_name, project_type):
    project_path = PROJECT_ROOT / project_type / project_name
    project_path.mkdir(parents=True, exist_ok=True)

    # Common folders
    os.makedirs(os.path.join(project_path, "data"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "results"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "notebooks"), exist_ok=True)


    # Copy sample data and notebook template
    templates_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    source_file = os.path.join(templates_path, "get_started.ipynb")
    dest_file = os.path.join(project_path, "notebooks", "get_started.ipynb")

    shutil.copy(source_file, dest_file)
    # Repo setup (optional, done later)
    return project_path

def create_github_repo(repo_name):
    g = Github(GITHUB_TOKEN)
    user = g.get_user()
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

def clone_and_setup_repo(repo_url, target_path, env_name, fallback_path):
    try:
        subprocess.run(["git", "clone", repo_url, str(target_path)], check=True)
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
