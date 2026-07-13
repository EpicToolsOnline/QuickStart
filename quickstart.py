import subprocess
import json
import sys
import os

def resource_path(relative_path):
    # When PyInstaller runs a bundled --onefile exe it unpacks any embedded
    # data files into a temp folder at runtime and stores that folder's
    # path in sys._MEIPASS. If that attribute doesn't exist were just
    # running as a normal .py file, so use the folder this script lives in.
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def load_catalog():
    with open(resource_path("apps.json")) as f:
        return json.load(f)

def get_own_filename():
    if getattr(sys, "frozen", False):
        path = sys.executable
    else:
        path = sys.argv[0]
    return os.path.basename(path)

def parse_requested_apps(filename, catalog):
    name_without_ext = os.path.splitext(filename)[0]
    tokens = name_without_ext.split(" ")
    tokens = tokens[1:]

    requested = {}
    for token in tokens:
        if token in catalog:
            requested[token] = catalog[token]
        else:
            print(f"Unknown app in filename, skipping: {token}")

    return requested

def install_apps(apps_to_install):
    results = []

    for token, info in apps_to_install.items():
        package_id = info["id"]
        display_name = info["name"]

        result = subprocess.run(
            [
                "winget", "install",
                "--id", package_id,
                "-e",
                "--silent",
                "--accept-package-agreements",
                "--accept-source-agreements"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            status = "installed"
        elif "No available upgrade found" in result.stdout:
            status = "already installed"
        else:
            status = "failed"

        results.append({"name": display_name, "status": status})
        print(f"{display_name}: {status}")

    return results


if __name__ == "__main__":
    catalog = load_catalog()
    own_filename = get_own_filename()
    apps_to_install = parse_requested_apps(own_filename, catalog)

    if not apps_to_install:
        print("No valid apps found in the filename, nothing to install.")
    else:
        install_apps(apps_to_install)