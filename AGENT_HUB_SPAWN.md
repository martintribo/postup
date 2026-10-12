# AGENT_HUB_SPAWN

Your session id is:

```
8da23588d372529b8c0178bb80e4b53e
```

Runtime: grok
Cwd: /home/main/.agenthub/worktrees/postup/postup-health

## First actions (do these before anything else)

1. Use MCP server **agent-hub** (tools: bus_hello, bus_send, bus_status, bus_peers).
2. Call **bus_hello** with:
   - id: the session id above
   - label: spawn-grok
   - cwd: /home/main/.agenthub/worktrees/postup/postup-health
3. Then execute the user task below.
4. When messaging another agent, use **bus_send** with from=your session id.
5. Keep the agent-hub inbox monitor running (Claude: plugin monitor; Grok: agent-hub-inbox skill).
6. If you must wait for a message and may not stay interactive, **poll** the local inbox
   until it arrives (do not just end the turn):
   GET http://127.0.0.1:3051/bus/inbox?session=8da23588d372529b8c0178bb80e4b53e
   Repeat every ~2s (Bash/PowerShell/curl) until you see the expected message, then act.

## User task

You are agent 8da23588d372529b8c0178bb80e4b53e (cwd /home/main/.agenthub/worktrees/postup/postup-health). folderKind: repo. Call bus_hello with this session id, then process any pending inbox messages (poll GET http://127.0.0.1:3051/bus/inbox?session=8da23588d372529b8c0178bb80e4b53e). Keep the agent-hub inbox monitor running.
