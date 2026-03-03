# MCP Tool Patterns & Workarounds

## Material Creation
### connect_nodes
- `targetNodeId` must be `"Main"` (not "Material", "root", or "output")
- Use `inputName` parameter (e.g., "BaseColor", "EmissiveColor"), NOT `targetPin`
- `sourcePin` should be `"RGB"` for color outputs

### Applying materials to actors
- `set_component_property` with `OverrideMaterials` SILENTLY FAILS
- C++ handler doesn't support FObjectProperty arrays (UMaterialInterface*)
- No dedicated `set_actor_material` MCP action exists yet
- WORKAROUND: None currently — needs C++ plugin modification

### Material paths
- `/Game/Materials/M_Name` may fail with PARENT_FOLDER_NOT_FOUND
- Use `/Game/M_Name` instead (root Content folder)

## Actor Spawning
- Actors spawned via MCP are in-memory only until saved
- `save_all` may not detect level actor changes — use Ctrl+Shift+S
- Always verify which level is active before spawning (get_current_level)
- /Temp/ levels are temporary and don't persist

## Concert + MCP
- DO NOT spawn/delete actors via MCP while in a Concert session unless explicitly asked
- MCP changes go into the shared Concert transaction log and affect ALL connected users
- Always ask before modifying the shared world

## Animation
- MCP can't modify AnimSequence properties (root motion settings)
- Montage creation via animation_physics tool has timeouts — BROKEN
- Slot node adding also broken
