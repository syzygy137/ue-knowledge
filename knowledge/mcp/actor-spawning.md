# Actor Spawning via MCP

## Basic spawn
```json
{
  "action": "spawn",
  "actorName": "MyActor",
  "classPath": "/Script/Engine.StaticMeshActor",
  "location": {"x": 0, "y": 0, "z": 100},
  "scale": {"x": 1, "y": 1, "z": 1}
}
```

## Important rules
1. Always check current level first (`get_current_level`) — don't spawn into /Temp/ levels
2. Actors are in-memory only until saved
3. DO NOT spawn while in Concert session unless explicitly asked — it affects all connected users
4. `save_all` may not save level actors — user must Ctrl+Shift+S

## set_game_mode
- Can crash the editor — always save first before calling
