---

## 🏃 Optional: Auto-change directory on environment activation

You can configure your Conda environment so that when you activate it, your shell automatically changes to your project folder:

1. Find your environment folder by running:
   ```powershell
   conda info --envs
   ```
   Look for the path next to your environment name (e.g., `ProjLab`).

2. Create a folder named `activate.d` inside your environment's `ProjLab\etc\conda` directory:
   ```powershell
   mkdir "<env_path>\etc\conda\activate.d"
   ```

3. Create a file named `auto_cd.bat` in that folder with the following content:
   ```bat
   cd /d <PATH/TO/YOUR/ProjLab>
   ```
4. For Windows users, you may need to make another file named `auto_cd.ps1` in the same folder  with the following content:
   ```ps1
   Set-Location -Path 'C:\Users\hamed\OneDrive\projects\ProjLab'
   ```

Now, every time you run `conda activate ProjLab`, your shell will automatically change to your project directory. Next time just activate ProjLab and run 
   ```powershell
      python init_proj.py
   ```

# ProjLab
**ProjLab** is a Python-based command-line tool for quickly scaffolding new projects with a consistent structure, optional GitHub integration, and Conda environment setup.  
It’s designed for developers, data scientists, and researchers who often switch between **temporary**, **proof-of-concept (PoC)**, and **production** projects.

---

## ✨ Features

- 📂 **Automatic folder structure** (`data/`, `results/`, `notebooks/`, `related-files/`, and optional `repo/`)
- 📓 Copies a starter Jupyter notebook into the `notebooks/` folder
- 🔗 Option to **clone an existing GitHub repo** or **create a new one**
- 🛠 **Environment management**:
  - Create a new Conda environment from scratch
  - Or build it from an existing `environment.yml`
- 🔑 Reads your GitHub **Personal Access Token (PAT)** from a `README.txt` in your projects root (on your local machine)
- 📌 Keeps your projects organized under "PROJECT_ROOT" by category (`tmp`, `poc`, `prod`)

---

## 📦 Requirements

- [Python 3.11+](https://www.python.org/downloads/)
- [Miniconda or Anaconda](https://docs.conda.io/en/latest/miniconda.html)
- [Git](https://git-scm.com/)
- [PyGithub](https://pypi.org/project/PyGithub/)
- [questionary](https://pypi.org/project/questionary/)
- A **GitHub Personal Access Token (PAT)** with `repo` scope

---

## ⚙️ Installation

1. **Clone this repo** (or download):
```bash
   git clone https://github.com/<your-username>/ProjLab.git
   cd ProjLab
```

3. **Create and activate a Conda environment from already provided yml file**:

   ```bash
   conda create create -f ProjLab.yml
   conda activate ProjLab
   ```

4. **Store your GitHub Username and PAT** in a `.env` file located in the `ProjLab` directory (Note: .env will not be synced to your repo.):

   ```
   GITHUB_USERNAME=your_github_username
   GITHUB_PAT_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 📁 Folder Structure

When you create a project, `ProjLab` will make:

```
PROJECT_ROOT/
└── project-type/         # tmp | poc | prod
    └── project-name/
        ├── data/
        ├── results/
        ├── notebooks/
        │   └── get_started.ipynb
        ├── related-files/
        └── repo/         # cloned GitHub repo (if chosen)
```

---

## 🚀 Usage

Run the tool:

```bash
conda activate ProjLab
python init_proj.py
```

You will be prompted for:

1. **Project name**
2. **Project type** (`tmp`, `poc`, `prod`)
3. Whether you **already have a GitHub repo**

   * If yes → enter repo URL → clone into `repo/`
   * If no → option to create a new repo in your GitHub account
4. **Environment setup**:

   * Use `environment.yml` from the repo if available
   * Or create a new Conda environment

---

## 🔐 Security

* Your GitHub PAT and username are **never stored in the script** — they are read from the `.env` file in the root of your projects folder.
* Make sure this file is **not committed to Git** by adding `.env` to `.gitignore` (already added).

---

## 🛠 Example Session

```plaintext
? Project name: my-analysis
? Project type: poc
? Do you already have a GitHub repo for this project? No
? Do you want to create a new GitHub repo? Yes
✅ Created new repo 'my-analysis'
? Do you want to create a new Conda environment for this project? Yes
📦 Creating Conda environment: my-analysis
✅ Project 'my-analysis' is ready at: C:\Users\YourName\projects\poc\my-analysis
```

---

## 📌 Tips

* Use `tmp` for scratch or throwaway work
* Store Data files in `data/`, write the results to `results/`, and store related-files (e.g., papers and presentations) in `related-files/` to avoid commiting them to git.
* Run `conda env export --no-builds > environment.yml` inside a project to save its dependencies for reproducibility

---

## 📜 License

MIT License — You are free to use and modify this tool.

