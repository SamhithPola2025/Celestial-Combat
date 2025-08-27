# Celestial Combat

Celestial Combat is a 2D/3D game built using [Ursina](https://www.ursinaengine.org/) and [Panda3D](https://www.panda3d.org/), with Python 3.12. The project includes custom sprites, audio, and interactive gameplay.

---

## Features

- Explore and fight enemies and bosses
- Collect coins and bananas
- Upgrade abilities via shop system
- Simple UI for health, coins, and actions
- Background music with multiple tracks

---

## Requirements

- Python 3.12
- Pip

Dependencies are listed in `requirements.txt`:

ursina==8.1.1
panda3d==1.10.15
numpy
pillow

---

## Setup

1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

And finally, run it!:
```bash
python main.py
python3 main.py
# the one you use depends on the type of python you have installed, just try both if you are unsure!
```

And thats the very easy instalation on how to get the game running quickly.
If there are any problems, open a issue or a PR, and I will get to it as soon as I can!

> **Note:** Currently, a standalone `.exe` or macOS app build isn’t provided. Ursina relies on Panda3D and certain system-level graphics/audio libraries that don’t always bundle cleanly with PyInstaller across platforms. We recommend running the game via Python in a virtual environment for now and either way it is a very easy process.
