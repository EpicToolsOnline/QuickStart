import subprocess
import json
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def load_catalog():
    try:
        with open(resource_path("apps.json")) as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: apps.json is missing, this build is broken.")
        input("Press Enter to exit...")
        sys.exit(1)
    except json.JSONDecodeError:
        print("ERROR: apps.json is corrupted and can't be read.")
        input("Press Enter to exit...")
        sys.exit(1)

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
            print(f"Unknown app in filename, skipping: {token} renember file names are case-sensitve.")

    return requested

def check_winget_available():
    try:
        subprocess.run(
            ["winget", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def install_apps(apps_to_install):
    results = []

    for token, info in apps_to_install.items():
        package_id = info["id"]
        display_name = info["name"]

        try:
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
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                status = "installed"
            elif "No available upgrade found" in result.stdout:
                status = "already installed"
            else:
                status = "failed"

        except subprocess.TimeoutExpired:
            status = "timed out"
        except Exception as e:
            status = f"error: {e}"

        results.append({"name": display_name, "status": status})
        print(f"{display_name}: {status}")

    return results


if __name__ == "__main__":
    catalog = load_catalog()

    if not check_winget_available():
        print("ERROR: winget isn't available on this system. QuickStart needs winget to work.")
        input("Press Enter to exit...")
        sys.exit(1)

    own_filename = get_own_filename()
    apps_to_install = parse_requested_apps(own_filename, catalog)

    if not apps_to_install:
        print("No valid apps found in the filename, nothing to install. Reminder: App names are Case-Sensitive")
        input("Press Enter to exit...")
    else:
        install_apps(apps_to_install)
        print()
        input("Done. Press Enter to exit...")