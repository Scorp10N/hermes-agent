# Devil's Advocate — Session Log

| Check | Date | Target | Score | Verdict |
|-------|------|--------|-------|---------|
| check-1 | 2026-06-09 | commit 61a4c6bba — mission-control MCP skill + config stub | 14/20 | Needs rework |

## check-1 highlights
- CRITICAL: tool names `mcp_mission-control_*` should be `mcp_mission_control_*` (Hermes sanitizes hyphens → underscores; verified mcp_tool.py:2818-2842).
- MAJOR: example `MC_API_KEY: ""` breaks auth; use `${MC_API_KEY}` (interpolation supported).
- MAJOR: "survives rebuilds" goal unverified — skill not yet in running image; needs `yantra hermes-build`.
- MINOR: hardcoded agent id=2 brittle; resolve via mc_list_agents.
- MINOR: header implies guaranteed registration, but the only shipped config (example) is commented out.
- Verified-clean: agent id=2 correct, MC reachable at mission-control:3000, lifecycle states valid, no secrets in diff, YAML parses.

Log: .devils-advocate/logs/check-1-critique-2026-06-09.md
