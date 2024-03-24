<style>
  img {
    border-radius: 10px;
  }
  .demo-container img {
    flex: 1;
    max-width: calc(33.33% - 10px); /* 3 images and shrink to create small gap between */
    height: auto; /* maintain aspect ratio */
  }
  .demo-container {
    display: flex;
    flex-wrap: none;
    justify-content: space-between;
  }
  span {
    display: inline-block;
    padding: 0px 5px;
    border-radius: 5px;
  }
  .redacted {
    color: white;
    background-color: black;
  }
  .dotnet {
    color: white;
    background-color: purple;
  }
</style>

<!-- Badge pills -->

![Python Version](https://img.shields.io/badge/Python-3.12.2-blue)

<!-- Demo -->
<div style="text-align: center">
  <h1>Game of Life v2</h1>
  <p>A speedrun of rewriting an old uni project</p>
</div>

<div class="demo-container">
  <img src="docs/images/gol-demo-settings-screen.gif">
  <img src="docs/images/gol-demo-simulation-screen.gif">
  <img src="docs/images/gol-demo-output.gif">
</div>

<!-- Main content -->

## Why ?

One of my old uni projects involved mocking the Software Development lifecycle while creating the classic _Game of Life_. The next step in my professional journey involves me automating <span class="redacted">[REDACTED]</span> using Python for **everything**. After writing predominantly React/.NET apps for the past year, I saw this as the perfect way to get wired into Python development again.

The following is a speedrun of rewriting my original <span class="dotnet">.NET</span> implementation of _Game of Life_ into an enhanced version - highly interactive and feature rich.

[See the original here (cringe warning)](https://github.com/johnnymadigan/game-of-life).

## Setup

- Use Python version >=3.12.2
- Recommend using **pyenv** (like **nvm**): `pyenv install 3.12.2`, `pyenv global 3.12.2`
- Setup virtual environment `python -m venv venv`
- Activate in VSCode or `source ./venv/bin/activate`
- Install dependencies `pip install -r requirements.txt`
- To run via CLI, main script needs execute perms: `chmod u+x game-of-life.py`
- Run `./game-of-life.py`

## Usage

```
(\(\
( . .) so how do I play ?
(づ🎮⊂)
```

- Settings can be passed via CLI args, see `./game-of-life -h`
- Initial settings are applied from CLI
- You can modify/reset to defaults in the main menu
- <kbd>↑</kbd> <kbd>↓</kbd> to navigate through settings
- Start typing to set new input for selected setting
- <kbd>←</kbd> <kbd>→</kbd> to cycle through fixed setting options
- <kbd>delete</kbd> to clear the input
- <kbd>enter</kbd> to save the input
- <kbd>tab</kbd> <kbd>tab</kbd> to reset
- <kbd>space</kbd> <kbd>space</kbd> to start
- <kbd>Ctrl</kbd> <kbd>C</kbd> to exit
- GIFs are saved in _./gifs_

## Dev notes

### _How do I debug ?_

- Use VSCode:

  ![venv]("docs/images/venv.png")

  ![debug]("docs/images/debug.png")

### _How do I run unit tests ?_

- Use VSCode:

  ![debug]("docs/images/tests.png")

### _How do I regen the dependency graph ?_

- Run `pipdeptree --graph-output png > dependencies.png`

## Dependency Graph

<img src="docs/images/dependencies.png">

- _curses_ for pretty screens + key events
- _numpy_ for merging multiple cell matrices (for ghost effect)
- _argparse_ for CLI args support
- _matplotlib_ + _pillow_ for creating GIF outputs
