---
name: mission-control
description: Use when coordinating tasks with other agents, checking task queue, reporting status, or interacting with Mission Control — the shared agent orchestration dashboard.
version: "1.0"
author: Scorp10N
license: MIT
metadata:
  hermes:
    tags: [Mission-Control, Tasks, Agents, Coordination, Orchestration]
    related_skills: [native-mcp]
---

# Mission Control

Shared agent orchestration dashboard. Tools are available via the `mcp_mission-control_*` prefix (MCP server auto-registered at startup from `/app/mc-mcp-server.cjs`).

Your agent ID in MC is **2** (hermes). Agent name: hermes.

## Key Tools

**Presence / Health**
- `mcp_mission-control_mc_health` — check MC is reachable
- `mcp_mission-control_mc_list_agents` — all registered agents and their status
- `mcp_mission-control_mc_heartbeat` — send heartbeat (id=2)

**Tasks**
- `mcp_mission-control_mc_list_tasks` — all active tasks
- `mcp_mission-control_mc_poll_task_queue` — pick up tasks assigned to hermes (agent_id=2)
- `mcp_mission-control_mc_get_task` — get full task details + comments
- `mcp_mission-control_mc_create_task` — create a new task
- `mcp_mission-control_mc_update_task` — update status or resolution
- `mcp_mission-control_mc_add_comment` — add a comment to a task
- `mcp_mission-control_mc_broadcast_task` — notify all agents about a task

**Agents**
- `mcp_mission-control_mc_get_agent` — get agent details by id
- `mcp_mission-control_mc_wake_agent` — wake a sleeping agent
- `mcp_mission-control_mc_read_memory` — read an agent's working memory
- `mcp_mission-control_mc_write_memory` — write to an agent's memory

**Knowledge Base**
- `mcp_mission-control_mc_search_knowledge` — full-text search across all knowledge files
- `mcp_mission-control_mc_read_knowledge_file` — read a specific knowledge file
- `mcp_mission-control_mc_write_knowledge_file` — create or update a knowledge file

## Task Lifecycle

```
inbox → assigned → in_progress → review → done
```

Move to `in_progress` when starting a task, `done` when complete (include a `resolution` field).

## First Moves

1. Check MC is up: `mcp_mission-control_mc_health`
2. Check task queue: `mcp_mission-control_mc_poll_task_queue` with agent_id=2
3. Pick up a task: `mcp_mission-control_mc_update_task` with `{"status":"in_progress"}`
