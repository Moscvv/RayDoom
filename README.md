# RayDoom

A 3D engine in Python, using Raylib and Binary Space Partitioning, inspired by DOOM (1993).

The base engine — camera, BSP-based rendering, texture mapping, and level loading — follows [StanislavPetrovV's DOOM-Clone tutorial](https://github.com/StanislavPetrovV/DOOM-Clone) ([video walkthrough](https://youtu.be/vdNrNCqT8No)). On top of that foundation, this project is an ongoing work and so far it has been added:

- **`UI.py`** — HUD and on-screen UI handling
- **`player.py`** — player state and movement separated into its own module
- **`collision_handler.py`** — dedicated collision-resolution logic, built independently of the base tutorial
- **`process_sprites.py` / `weapon_sprite.py`** — sprite rendering and weapon-view systems

## Current Status

The engine runs, renders levels via BSP raycasting, and handles sprites and weapons. Collision has some bugs — the player can occasionally clip through geometry or catch on wall edges —.

## Roadmap

- [ ] Harden collision detection across all wall geometries
- [ ] Polish sprite/weapon rendering
- [ ] Add enemy AI
- [ ] Sound support
- [ ] Additional levels

## Why this project

Because is fun and I Love the idea of recreating a videogame for 0.

 Understand how a raycasting/BSP renderer like DOOM's actually works it's been super fun. As a fan, seeing aspecs you do not see In the surface it's amazing, also this is polishing further my Python knowledge and problem-solving.

## Credits

- Original engine tutorial and base architecture: [StanislavPetrovV/DOOM-Clone](https://github.com/StanislavPetrovV/DOOM-Clone)
- DOOM (1993) by id Software — this is a fan learning project, not affiliated with or endorsed by id Software or Bethesda.

## License

MIT — see [LICENSE](LICENSE). This project builds on code and structure from the tutorial linked above; if you reuse this code, please also credit the original tutorial.