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

Shared agent orchestration dashboard. Tools are registered as `mcp_mission_control_*` (Hermes sanitizes server name hyphens to underscores). Requires `mcp_servers.mission-control` enabled in `config.yaml` — see the stub in `cli-config.yaml.example`.

Your agent name in MC is **hermes**. Resolve your numeric ID on first use via `mcp_mission_control_mc_list_agents` (filter by name=hermes) rather than assuming a hardcoded value.

## Key Tools

**Presence / Health**
- `mcp_mission_control_mc_health` — check MC is reachable
- `mcp_mission_control_mc_list_agents` — all registered agents and their status
- `mcp_mission_control_mc_heartbeat` — send heartbeat (pass your resolved id)

**Tasks**
- `mcp_mission_control_mc_list_tasks` — all active tasks
- `mcp_mission_control_mc_poll_task_queue` — pick up tasks assigned to hermes (pass your resolved agent_id)
- `mcp_mission_control_mc_get_task` — get full task details + comments
- `mcp_mission_control_mc_create_task` — create a new task
- `mcp_mission_control_mc_update_task` — update status or resolution
- `mcp_mission_control_mc_add_comment` — add a comment to a task
- `mcp_mission_control_mc_broadcast_task` — notify all agents about a task

**Agents**
- `mcp_mission_control_mc_get_agent` — get agent details by id
- `mcp_mission_control_mc_wake_agent` — wake a sleeping agent
- `mcp_mission_control_mc_read_memory` — read an agent's working memory
- `mcp_mission_control_mc_write_memory` — write to an agent's memory

**Knowledge Base**
- `mcp_mission_control_mc_search_knowledge` — full-text search across all knowledge files
- `mcp_mission_control_mc_read_knowledge_file` — read a specific knowledge file
- `mcp_mission_control_mc_write_knowledge_file` — create or update a knowledge file

## Task Lifecycle

```
inbox → assigned → in_progress → review → done
```

Move to `in_progress` when starting a task, `done` when complete (include a `resolution` field).

## First Moves

1. Check MC is up: `mcp_mission_control_mc_health`
2. Resolve your agent id: `mcp_mission_control_mc_list_agents` → find entry with name=hermes
3. Check task queue: `mcp_mission_control_mc_poll_task_queue` with your agent_id
4. Pick up a task: `mcp_mission_control_mc_update_task` with `{"status":"in_progress"}`
