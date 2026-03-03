# Animation System

## Meshy AI Animations
- Meshy AI anims have no proper root bone — Hips IS the root
- Root motion locks kill all motion because Hips contains all translation+rotation
- Need AnimBP with Transform(Modify)Bone to strip Hips translation

## AnimBlueprint Setup
- ABP_Hero created at /Game/Blueprints/ABP_Hero but NOT wired up yet
- PlayAnimation mode works for basic playback without AnimBP

## MCP Limitations
- Can't modify AnimSequence properties (root motion settings)
- Montage creation via animation_physics tool has timeouts (BROKEN)
- Slot node adding also broken
