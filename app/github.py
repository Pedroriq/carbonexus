import os
import subprocess
import git
from git import rmtree
import platform


class Repository:
    def __init__(self, link):
        self._link = link

    def clone_repo(self):
        actual_dir = os.getcwd()
        repository_dir = os.path.join(actual_dir, 'repository_git')

        if os.path.exists(repository_dir):
            rmtree(repository_dir)

        print(f"Clonando o repositório {self._link}...")
        git.Repo.clone_from(self._link, repository_dir)
        print(f"Repositório clonado em {repository_dir}.")
        self.install_dependencies(repository_dir)

    @staticmethod
    def install_dependencies(repo_dir):
        requirements_path = os.path.join(repo_dir, "requirements.txt")
        if os.path.exists(requirements_path):
            print("Instalando dependências...")
            os.chdir(repo_dir)
            subprocess.run(["python", "-m", "venv", "venv"])
            if platform.system() == "Windows":
                pip_executable = os.path.join(repo_dir, 'venv', 'Scripts', 'pip.exe')
                subprocess.run([pip_executable, "install", "-r", requirements_path])
            os.chdir('..')
            print(os.getcwd())
        else:
            print("Nenhum requirements.txt encontrado.")

    def start(self):
        self.clone_repo()