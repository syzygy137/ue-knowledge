# Materials via MCP

## Creating Materials
```json
{
  "action": "create_material",
  "path": "/Game/M_MyMaterial"
}
```
- Use `/Game/M_Name` not `/Game/Materials/M_Name` (parent folder may not exist)

## Connecting Nodes
```json
{
  "action": "connect_nodes",
  "targetNodeId": "Main",
  "inputName": "BaseColor",
  "sourcePin": "RGB"
}
```
- `targetNodeId` MUST be `"Main"`
- Use `inputName` not `targetPin`

## Applying Materials to Actors
**DOES NOT WORK via MCP** — `set_component_property` with `OverrideMaterials` silently fails.
The C++ handler can't set FObjectProperty arrays. Needs a dedicated `set_actor_material` action in the plugin.
