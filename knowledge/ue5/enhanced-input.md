# Enhanced Input System

## Assets needed
- **Input Actions**: IA_Move (Axis2D), IA_Look (Axis2D), IA_Jump (Digital)
- **Input Mapping Context**: IMC_Default with WASD/Mouse2D/SpaceBar bindings

## DefaultGame.ini config
```ini
+DefaultMappingContexts=(InputMappingContext="/Game/Input/IMC_Default.IMC_Default",Priority=0)
```

## Gotchas
- Assets created via MCP are in-memory only — must save_all
- Need to recreate each session if not saved to disk
