import subprocess
import json
import sys
import os
import threading

BANNER = r"""
+----------------------------------------+
|                                          |
|   Q U I C K S T A R T                   |
|                                          |
|   created by epictoolsonline.com        |
|                                          |
+----------------------------------------+
"""

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
            print(f"Unknown app in filename, skipping: {token} remember file names are case-sensitive.")

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

def install_one_app(package_id):
    # Not using capture_output here on purpose: that buffers everything until
    # the process ends, which is exactly why installs looked "frozen" before.
    # Streaming line by line lets winget's own progress print live instead.
    process = subprocess.Popen(
        [
            "winget", "install",
            "--id", package_id,
            "-e",
            "--silent",
            "--accept-package-agreements",
            "--accept-source-agreements"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Streaming removes subprocess.run's built-in timeout, so this timer
    # does the same job: kill the process if it hangs past 5 minutes.
    timer = threading.Timer(300, process.kill)
    timer.start()

    output_lines = []
    try:
        for line in process.stdout:
            print(line, end="")
            output_lines.append(line)
        process.wait()
    finally:
        timer.cancel()

    output_text = "".join(output_lines)

    if process.returncode == 0:
        return "installed"
    elif "No available upgrade found" in output_text:
        return "already installed"
    elif process.returncode is None:
        return "timed out"
    else:
        return "failed"

def install_apps(apps_to_install):
    results = []

    for token, info in apps_to_install.items():
        display_name = info["name"]
        print(f"\nInstalling {display_name}...")
        print("-" * 40)

        try:
            status = install_one_app(info["id"])
        except Exception as e:
            status = f"error: {e}"

        results.append({"name": display_name, "status": status})
        print(f"-> {display_name}: {status}")

    return results


if __name__ == "__main__":
    print(BANNER)

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
        results = install_apps(apps_to_install)
        print("\n" + "=" * 40)
        print("Done. Summary:")
        for r in results:
            print(f"  {r['name']}: {r['status']}")
        input("\nPress Enter to exit...")