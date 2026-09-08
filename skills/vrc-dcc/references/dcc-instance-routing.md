# Choose a DCC execution route from observed capabilities

Use for a named World/avatar task when an existing Editor is busy, a connection
is ambiguous, or a worker needs an independent file-based route. Recover the
current project's writer and authorized write set first.

| Work | Useful route | Evidence before claiming it works |
|---|---|---|
| Design, source inspection, material inventory | Files and offline tools | Named input revision, outputs and scope; no Editor startup needed |
| Mesh generation or conversion in owned files | Installed Blender background Python when the job permits it | Child executable/version, isolated settings/output paths, exit status/log and saved-file readback |
| Interactive scene inspection/editing | Discovered native MCP or installed provider CLI/SDK | Selected instance plus current project/document/scene readback |
| Multiple GUI or MCP targets | Only when that installed client and addon support independent targeting | Separate endpoints where required, explicit target selection, identity readback and reconnect behavior verified for each |

Blender's command-line background/Python capability does not establish that a
particular MCP addon can start without its GUI. Check the installed addon's
background checks, auto-start behavior, port selection and client's connection
cache. A single global connection or a hard-coded port is a limitation to resolve
for that implementation, not evidence that Blender cannot run independent jobs.

For a background worker, use task-owned configuration/preferences, temporary
files, logs and output directories, with environment overrides confined to the
child process. Check local executable help for supported options and argument
order; loading a file after setting options may change the state used by a
later command. Choose CPU/GPU work consistent with current resource use and
the owner's task scope. Do not reconfigure or close another writer's instance.

A listening port, process command line, MCP session or a successful connection
is not the current `.blend` file or Unity project identity. Select an observed
instance and read back its current file/project/scenes before mutation. Repeat
after reconnect or another operation that can change the target. After a timeout,
inspect the effect before retrying. A connection receipt is not a writer lock.

Keep capability, source inspection and local demonstration separate in the
handoff. Use existing project bridges/builders when supported; proposed station
`world_*` adapters are not a prerequisite. See
[World production](../../../docs/WORLD_PRODUCTION.md) and [lazy MCP](../lazy-mcp.md).

Blender documents command-line arguments in its
[manual](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html).
Use the version matching the installed executable; this workflow does not assert
that a particular MCP package supports headless or multiple-target operation.
