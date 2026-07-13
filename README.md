# QuickStart

An open source, Ninite-style batch installer for Windows. Pick apps on the website, download an exe, run it, it installs everything you picked using winget in the background. No wizards, no bundled junk, no clicking through fifteen installers by hand.

This repo is the actual installer app. The website that generates the download lives in a separate repo, [QuickStart Web](https://github.com/EpicToolsOnline/QuickStartWeb), see below for how the two connect.

## How it works

QuickStart doesn't use a config file or ask you anything at runtime. The apps you want are baked into the filename of the exe itself. A file named `QuickStart Chrome Discord VSCode.exe` installs Chrome, Discord, and VS Code, nothing else. The website builds that filename for you, but you can also just rename the exe yourself by hand, no website required, as long as the words in the filename match the app names in `apps.json` exactly (case-sensitive).

Under the hood, each app name in the filename gets matched against `apps.json`, which maps a short name to its real winget package ID. It then runs `winget install` for each match, with flags to keep it silent and skip license prompts.

## How QuickStart and QuickStart Web connect

These are two separate repos on purpose, one's a desktop app, the other's a website, different tech, different deploy targets. But they share one important dependency: **the app list.**

`apps.json` in this repo is the master list QuickStart actually knows how to install. `index.astro` in the [QuickStart Web](https://github.com/EpicToolsOnline/QuickStartWeb) repo is what shows checkboxes on the website.

**These two lists are edited separately and don't sync automatically.** If you add an app to `apps.json` here, it will not show up as a checkbox on the website until someone also adds it to `index.astro` in QuickStart Web. The app will still work if someone manually renames the exe to include it, since the exe only reads `apps.json`, it just won't be pickable through the website's UI until both files are updated.

If you're contributing a new app, please try to update both repos together, or at least flag in your PR that the sister repo needs the same update.

## Contributing

### Adding an app

Easiest contribution there is. Open `apps.json` and add an entry:

```json
"Firefox": {"id": "Mozilla.Firefox", "name": "Mozilla Firefox"}
```

The key is what appears in the filename (letters, numbers, `+`, `-` only, no spaces). `id` is the exact winget package ID, find it with `winget search <app name>` in a terminal. `name` is the display name shown in output.

Remember to also add it to `index.astro` over in [QuickStart Web](https://github.com/EpicToolsOnline/QuickStartWeb) if you want it selectable on the site.

### Code changes

Fork the repo, make your changes on a branch, open a pull request. All PRs need an approving review before they can merge, that's enforced by branch rules, not just a suggestion.

### Reporting a bug

Open an issue. Include what app you were trying to install, what the console output said, and your Windows version if relevant.

## Building the exe yourself
```py
"python -m PyInstaller --onefile --add-data "apps.json;." quickstart.py"
```
Output lands in `dist/quickstart.exe`.

## Requirements

Windows 10/11 with winget installed (built in on most modern setups).

## License

MIT, see [LICENSE](LICENSE). Use it, modify it, redistribute it, just keep the copyright notice intact.
