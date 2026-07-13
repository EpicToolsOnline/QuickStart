# QuickStart

An open source, Ninite-style batch installer for Windows. Pick the apps you want off the site, download the exe, run it, and it installs everything you picked using winget in the background. No bloatware, no toolbars, no clicking through install wizards fifteen times when you're setting up a new PC.

## How it actually works

QuickStart doesn't use a config file or ask you anything when it runs. The apps you want are baked straight into the filename of the exe itself. So a download named `QuickStart Chrome Discord VSCode.exe` will install Chrome, Discord, and VS Code, nothing else. The website builds this filename for you based on what you tick, you never have to touch it yourself.

Under the hood it's just calling `winget install` for each app, with the right flags to keep it silent and skip license prompts. If winget's not available on your system, or something's missing, it'll tell you and pause so you can actually read what happened instead of the window vanishing instantly.

## Why this exists

Ninite's great but it's closed source and you don't get to see or add to the app list yourself. This is the same idea, but the whole thing's out in the open, anyone can see exactly what it's doing, and anyone can add apps or fix bugs.

## Contributing

Adding an app is genuinely the easiest contribution you can make. Open `apps.json` and add an entry like this:

```json
"Firefox": {"id": "Mozilla.Firefox", "name": "Mozilla Firefox"}
```

The key is what shows up in the filename, `id` is the exact winget package ID (find it with `winget search <app name>` in a terminal), and `name` is what gets displayed to the user when it installs.

For anything else, code fixes, better error handling, whatever, fork the repo and open a pull request. All PRs need review before merging, so don't be shy about opening one even if it's a small change.

## Requirements

Windows 10/11 with winget installed (comes built in on most modern setups). That's it.

## License

MIT, see [LICENSE](LICENSE). Basically: use it, modify it, redistribute it, just keep the copyright notice to epictoolsonline.com intact.
