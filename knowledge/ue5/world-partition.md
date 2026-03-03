# World Partition & Levels

## How World Partition Works
- .umap files are intentionally small (~13KB) — this is normal
- Actors stored as individual .uasset files in `__ExternalActors__/<LevelName>/`
- 138 actors = 138 separate files in hex-named subdirectories
- The directories (0-9, A-F) are a hash-based structure for the actor files

## Level Paths
- `/Game/<LevelName>` — saved levels (persistent)
- `/Temp/<LevelName>` — temporary levels (lost on restart)
- Always check current level with `get_current_level` before spawning actors

## Saving
- Ctrl+Shift+S saves level actors to disk
- MCP `save_all` may report "0 dirty assets" even when level has unsaved actor changes
- Always verify saves by checking `__ExternalActors__/` directory for .uasset files
