import subprocess
import json

def install_apps(filename):
    with open(filename) as f:
        apps = json.load(f)

    results = []

    for name, package_id in apps.items():
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

        results.append({"name": name, "status": status})
        print(f"{name}: {status}")

    return results


if __name__ == "__main__":
    install_apps("chosenapps.json")