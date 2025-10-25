# Maze Explorer Game

Immerse yourself in a procedurally generated maze built with [Jac](https://github.com/Jaclang/jac) where every run feels different. Explore rooms, collect treasure, fend off threats, and escape through the exit—optionally aided by AI-generated hints powered by Gemini via [ByLLM](https://pypi.org/project/byllm/).

## Features

- Randomized maze carved at runtime with unique room descriptions
- Lightweight text-based interface with simple movement commands
- Health, treasure, monsters, and traps to keep each game tense
- Optional Gemini-powered hint system to nudge you toward the exit

## Prerequisites

- Python 3.11+ (tested with 3.12)
- Jac toolchain (`pip install jaclang`)
- Project dependencies (including `byllm`) installed in your virtual environment

> **Tip:** The repo often uses a virtual environment at `venv/`. Activate it (`source venv/bin/activate`) before running commands.

## Installation

```bash
# from the project root
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install jaclang byllm litellm
```

If you already have a `requirements.txt` or `poetry.lock` in your setup, use that instead of the ad‑hoc list above.

## Running the Game

```bash
source venv/bin/activate  # if not already active
jac run main.jac
```

You can quit any time by typing `quit` at the prompt.

### Controls at a Glance

| Command | Description |
|---------|-------------|
| `north`, `south`, `east`, `west` | Move through available exits |
| `status` | View current health, treasure, key, and steps |
| `map` | Review the list of rooms you have visited |
| `help` | Display basic command list |
| `hint` | Request an AI-generated hint (requires configured API key) |
| `quit` | End the current run |

## Enabling AI Hints (Gemini)

The `Player` walker uses ByLLM to call Gemini for contextual hints. The model looks for an API key in the environment—set one of the following variables before launching the maze:

```bash
# choose one of these variable names
export GOOGLE_API_KEY="your-gemini-key"
# or
export GEMINI_API_KEY="your-gemini-key"
```

Only one needs to be defined. Keep secrets out of source control—store them in a protected dotfile (e.g. `~/.config/maze-secrets.env`) and `source` it from your shell startup script:

```bash
mkdir -p ~/.config
install -m 600 /dev/null ~/.config/maze-secrets.env
echo 'export GOOGLE_API_KEY="your-gemini-key"' >> ~/.config/maze-secrets.env
echo 'source ~/.config/maze-secrets.env' >> ~/.bashrc
```

Launching the maze without a key is perfectly fine—the game will simply skip AI hints and remind you once per run.

## Troubleshooting

- **"AI hint unavailable" message every turn** – Ensure the environment variable is set *before* starting the game and that you restarted the shell after editing your startup files.
- **Import errors for Jac or ByLLM** – Confirm your virtual environment is active and reinstall dependencies (`pip install jaclang byllm`).
- **Weird maze layouts or difficulty spikes** – The maze is random! Reset with `Ctrl+C` or rerun the entry script.

## Next Steps

- Add automated tests for maze generation and walker logic
- Extend the hint system with richer context or multi-step guidance
- Experiment with alternative models supported by ByLLM/LiteLLM
