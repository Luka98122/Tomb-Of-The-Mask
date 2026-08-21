# Tomb of The Mask

<p align="center">
  <img width="400" height="400" alt="Trailer" src="https://github.com/user-attachments/assets/7bfd9188-6352-41ae-b566-22a296845ebc" />
</p>
---

A recreation of the popular web and mobile game *Tomb of The Mask*, built with pygame.
Mini project from [PFE Feb '25](https://pfe.rs).

## Running

Requires Python 3 and pygame:

```bash
pip install pygame
python main.py
```

## Controls

Arrow keys dash in a direction. You keep going until you hit a wall, so every move is
a commitment — collect the coins and stars on the way and reach the exit without
touching a spike or a death wall.

<img width="800" height="800" alt="Completion" src="https://github.com/user-attachments/assets/51cc2a9c-aa5c-4f31-9e96-3a885a5a6bf0" />

## Level editor

`helper.py` is the level editor used to build the maps:

```bash
python helper.py
```

Left click paints the currently selected tile, right click erases, and the palette
along the edges picks what you're painting (walls, coins, stars, start, exit).
Hold space to show the grid. The map is saved back to `maps/1.json` when you close
the window.

## Demos

Full video walkthroughs live in [`demos/`](./demos):

- `completion.mp4` — a full playthrough
- `speedrun.mp4` — a speedrun
- `editor.mp4` — the level editor in use

## Project structure

```
main.py     the game
helper.py   level editor
levels/     playable levels (JSON grids)
maps/       editor working files
cont/       sprites, font, and audio
demos/      video demos
```
