import subprocess
import os

def activateVenv(venv_location):
    # Command to activate the virtual environment
    activate_script = os.path.join(venv_location, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_location, "bin", "activate")

    # Run the activation and any other commands (if needed)
    subprocess.call(f"{activate_script}", shell=True)
