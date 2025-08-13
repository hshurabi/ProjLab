# projectgen

**projectgen** is a Python-based command-line tool for quickly scaffolding new projects with a consistent structure, optional GitHub integration, and Conda environment setup.  
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
   git clone https://github.com/<your-username>/projectgen.git
   cd projectgen
```

3. **Create and activate a Conda environment**:

   ```bash
   conda create -n projectgen python=3.11
   conda activate projectgen
   ```

4. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   *(If no `requirements.txt` exists yet, manually install `PyGithub` and `questionary`)*

5. **Store your GitHub PAT** in a `README.txt` located in your projects root (one level above `projectgen/`):

   ```
   Current Github PAT: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
       expires on YYYY/MM/DD
   ```

---

## 📁 Folder Structure

When you create a project, `projectgen` will make:

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
conda activate projectgen
python new_project.py
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

* Your GitHub PAT is **never stored in the script** — it’s read from `README.txt` in the root of your projects folder.
* Make sure this file is **not committed to Git** by adding it to `.gitignore`.

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

