import sys
import subprocess
import os


def create_and_setup_venv(venv_path, packages):
    """
    Creates a virtual environment, upgrades pip, and installs specified packages.
    
    Parameters:
        venv_path (str): Path to the virtual environment.
        packages (list): List of Python packages to install.
    """
    # Create the virtual environment
    print(f"Creating virtual environment at: {venv_path}...")
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    
    # Define paths for pip and activation script
    if os.name == "nt":  # Windows
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
        
    else:  # macOS/Linux
        pip_path = os.path.join(venv_path, "bin", "pip")
        
    # Upgrade pip inside the virtual environment
    print("Upgrading pip...")
    subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)

    # Install required packages
    print(f"Installing packages: {', '.join(packages)}...")
    subprocess.run([pip_path, "install"] + packages, check=True)


