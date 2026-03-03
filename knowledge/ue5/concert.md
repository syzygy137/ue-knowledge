# Concert Multi-User Editing

## What it is
Collaborative level editing (like Google Docs for UE). NOT multiplayer gameplay.

## How it works
- Shared transaction log in memory on a server
- When you join, it replays all transactions on top of your local disk state
- Only syncs the currently open level — other levels/assets on someone's disk don't transfer
- Both users can PIE independently but can't spectate each other

## Persistence
- Concert transactions are IN MEMORY ONLY
- If session is deleted/restarted, unsaved changes are LOST
- `save_all` via MCP returns "0 dirty assets" for level actor changes — doesn't detect them
- Must use Ctrl+Shift+S manually to save level actors to disk
- World Partition stores actors as separate .uasset files in `__ExternalActors__/<LevelName>/`
- A small .umap (13KB) is normal — actors are stored separately

## UDP Messaging Config
```ini
[/Script/UdpMessaging.UdpMessagingSettings]
EnabledByDefault=True
EnableTransport=True
UnicastEndpoint=0.0.0.0:6668
MulticastEndpoint=230.0.0.1:6666
+StaticEndpoints=<OTHER_PERSONS_IP>:6668
```
- UnicastEndpoint MUST be different port than MulticastEndpoint (6668 vs 6666) or socket bind fails
- StaticEndpoints port must match the OTHER person's UnicastEndpoint port

## Gotchas
- Opening Concert browser as a floating window can crash D3D12 on RTX 50-series (NvPresent64 crash)
- Dock the Concert browser into the main editor window to avoid this
- Last-write-wins for conflicts — no merge
- RAM usage grows over long sessions (transaction log) — reconnect to reset
