# Optional upstream update / local feedback record

Keep a filled copy with the project's existing private handoff. Existing records
with these facts are sufficient; this is not a new mandatory task system.
Method: [upstream-updates.md](../skills/vrc-dcc/references/upstream-updates.md).

## Scope and evidence

- Requested outcome / why this update matters:
- Project root, writer and owned paths:
- Source repository, actual remote/default branch:
- Last checked time and candidate commit:
- Previous integration evidence (per-file baseline where needed):
- Current local Git HEAD/status, or non-Git backup and relevant hashes:
- Comparison receipt / relevant source commits:

## Decisions per file or feature

| Source path + baseline | Local path | Candidate | Adopt / adapt / defer / keep local | Reason, dependencies, unresolved hunks |
|---|---|---|---|---|
| | | | | |

Optional machine mapping: [UPSTREAM_FILES.example.json](UPSTREAM_FILES.example.json).
Do not replace an unknown baseline with today's source HEAD. Different copied
files can retain different baselines. A relative link does not prove an agent
has consumed its latest content.

## Actual integration

- Local commit or resulting file hashes:
- Validation performed, result and artifact paths:
- Remaining engine/client/consumer checks:
- Baselines advanced for reconciled files; partial changes still pending:
- Prompt/task revision consumed by the next producer, if relevant:
- Next action and owner:

Keep candidate and integrated revisions separate. Preserve completed task cards
and original producer returns; append a coordinator decision or create a new
revision. Do not claim every consumer was updated because the source was pushed.

## Portable feedback to the source (when useful)

- Concrete trigger, previous behavior and resulting behavior:
- General mechanism, supported versions and feature paths:
- Patch/proposal and minimal reproduction, with actual checks:
- Project-specific assumptions removed or kept as explicit options:
- Source issue/PR/commit after maintainer review:
- Originating project's reconciliation/receipt after the source lands:

Keep private project assets and identifiers out of a public contribution. Reuse
the owner's established publication authorization and remote convention.
