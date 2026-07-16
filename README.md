# RayDoom

A 3D engine in Python, using Raylib and Binary Space Partitioning, inspired by DOOM (1993).

This project was built by following [StanislavPetrovV's DOOM-Clone tutorial](https://github.com/StanislavPetrovV/DOOM-Clone) ([video walkthrough](https://youtu.be/vdNrNCqT8No)), then extended with additional systems on top of it.

## Status: Work in Progress / Unfinished

This is a learning project, not a finished game. Expect bugs, missing features, and rough edges. It's shared as-is for anyone curious how a raycasting/BSP engine like this comes together in Python.

### Known Issues

- **Collision detection is bugged.** The current implementation in `collision_handler.py` doesn't reliably resolve player-vs-wall collisions in all cases — you may clip through geometry or get stuck on edges. This is the top priority fix.
- Other systems (sprites, weapons, UI) are functional but not fully polished.
- **Stairs (portal floor-height transitions) partially fixed (WIP):**
  - Fixed: a scheduled camera-height adjustment that was set but never applied (`apply_height_adjust` now exists in `camera.py`).
  - Fixed: the height adjustment re-triggering every frame instead of once per crossing.
  - Fixed: `Player.move()` and `Camera.move()` both independently running collision/movement each frame, causing duplicate checks — `Camera.move()` is now disabled, `Player` owns horizontal movement.
  - Still broken: `_get_player_current_sector()` / `_point_in_sector()` in `collision_handler.py` is a placeholder that always returns `True`, so it can't reliably tell which side of a portal the player is on. A local cross-product side-test (`_is_entering_back`) works for isolated single steps but breaks down in tighter areas with multiple nearby segments.
  - Next step: replace sector detection with proper point-location via the BSP tree in `bsp/`, instead of the per-segment side-test.

### What's added on top of the original tutorial

The base engine (camera, BSP rendering, textures, level loading) follows the tutorial closely. On top of that, this project adds:

- `UI.py` — basic UI/HUD handling
- `collision_handler.py` — dedicated collision logic (currently buggy, see above)
- `player.py` — player state separated out into its own module
- `process_sprites.py` / `weapon_sprite.py` — sprite and weapon rendering

## Roadmap

- [ ] Fix collision detection
- [ ] Clean up sprite/weapon rendering
- [ ] Add proper enemy AI (if attempted)
- [ ] Sound support
- [ ] More levels

## Credits

- Original engine tutorial and base architecture: [StanislavPetrovV/DOOM-Clone](https://github.com/StanislavPetrovV/DOOM-Clone)
- DOOM (1993) by id Software — this project is a fan learning exercise and is not affiliated with or endorsed by id Software or Bethesda.

## License

MIT — see [LICENSE](LICENSE). This project builds on code and structure from the tutorial linked above; if you reuse this code, please also credit the original tutorial.
