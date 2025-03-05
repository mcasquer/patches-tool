import subprocess
import os

def install_dependencies():
    """Install dependencies for the project."""
    subprocess.run(['dnf', 'install', '-y', 'git'], check=True)


def clone_repos():
    """Clone the required repositories if they don't exist."""
    repos = {
        'qemu': 'https://gitlab.com/qemu-project/qemu.git',
        'linux': 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git'
    }

    for repo_name, repo_url in repos.items():
        repo_path = os.path.join(os.getcwd(), repo_name)
        if not os.path.exists(repo_path):
            print(f"Cloning {repo_name}...")
            subprocess.run(['git', 'clone', repo_url], check=True)
        else:
            print(f"{repo_name} already exists. Skipping clone.")

def main():
    """Run the setup process."""
    install_dependencies()
    clone_repos()

# Only execute setup tasks if running this script directly
if __name__ == "__main__":
    main()

