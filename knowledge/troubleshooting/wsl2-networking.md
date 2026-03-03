# WSL2 ↔ Windows Networking for MCP

## MCP Connection
- UE plugin listens on `0.0.0.0:8090` (configured in DefaultGame.ini)
- MCP server on WSL2 connects to Windows gateway IP (e.g., `172.22.0.1:8090`)
- `bAllowNonLoopback=True` required for 0.0.0.0 binding
- `MCP_AUTOMATION_ALLOW_NON_LOOPBACK=true` in .mcp.json env

## Finding the Windows gateway IP from WSL2
```bash
cat /etc/resolv.conf | grep nameserver | awk '{print $2}'
```
Or:
```bash
ip route | grep default | awk '{print $3}'
```

## Firewall
- Windows Firewall may block WSL2 → Windows connections
- May need to add inbound rule for port 8090
