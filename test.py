import subprocess

result = subprocess.run(
    ["winget", "install", "--id", "Notepad++.Notepad++", "-e"],
    capture_output=True,
    text=True
)

print(result.stdout)
print("Success!" if result.returncode == 0 else "Something went wrong")