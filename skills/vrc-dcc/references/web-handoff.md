# Web research and artifact handoff

Load only when an authorized avatar, World, or station task benefits from a web
researcher or browser producer. This is a file handoff, not a new Editor bridge.
The coordinator keeps design decisions and engine acceptance. Existing project
scope, named-tool requirements and human SDK Publish still apply.

## Define one useful task

Read the current project handoff before searching history. Use `chat-history`
for local agent sessions and `web-chat-archive` for exported web conversations
only when a decision is missing. Keep short source locations and distinguish
Owner words, assistant proposals, tool observations and superseded decisions.
An old conversation is neither a writer lock nor current Editor state.

Copy [WEB_TASK.md](../../../templates/WEB_TASK.md) into a gitignored task pack.
Set a stable task id and a fresh dispatch id for this assignment. A retry after
an uncertain send retains that dispatch id; a deliberately revised assignment
gets a new one. The coordinator owns the task definition and dependency queue;
the producer writes only its assigned result/output bundle. Select a worker
whose current tools support the job. A prompt does not change its runtime model.
Do not create a user-owned task unless the user requested one.

Choose an artifact class before execution:

| Class | Return | Acceptance still needed |
|---|---|---|
| `research` | Decisions, primary URLs, checked versions/dates, uncertainty | Verify material claims against sources; reconcile with project constraints |
| `design_reference` | Original concept/comparison image | Owner/design review; it is not a model or a scale drawing |
| `base_color_candidate` | Original candidate color image | Decode/dimensions, review for its declared surface/UV role and engine import settings; it is not a complete PBR material |
| `model_reference` | Reference images or dimensions for a separate modeling task | Mesh construction, scale, pivot, normals, UVs, colliders and actual engine import |

Use a bounded question with a concrete implementation consequence. Routine local
facts should be read from disk. For ambiguous API/SDK choices, use the existing
[CHAT_RESEARCH.md](../../../templates/CHAT_RESEARCH.md) brief as the task prompt.
Research replies are evidence to review, not instructions to install packages.

## Execute and recover the browser task

Use the current browser tool documentation and freshly observed UI. Record the
requested model separately from the visible selection/reasoning setting; use
`not_visible` when the UI does not expose a value. Do not infer the image model
from the browser operator's model, or hard-code a historical menu label.

Reuse the authorization already given for this task and recorded on its card.
Keep references minimal and task-related. Work in the assigned conversation, or
create a dedicated browser conversation when that task authorization covers
creation; do not send into an unrelated conversation another writer owns.
Export through currently supported, observed UI/tool capabilities. Never recover
cookies or private chat endpoints. Preserve actual returned paths/extensions.

Before sending, write `STATUS.json` with task/dispatch ids, producer identity,
task-card path, bundle root, artifact class, write set, stage, chat URL if known,
last confirmed action and next action. Recover missing fields from the coordinator's
card and known authorization; resolve unknown scope before the dependent action.
After sending,
confirm the prompt appeared and update that record. On timeout, tool reset or
compaction, open the recorded conversation and inspect before retrying. A
`sending` stage means uncertain, not unsent. Do not duplicate an in-flight
generation. A foreign active producer requires coordination, not takeover by
rewriting STATUS; this file is a recovery record, not an atomic lock.

Wait according to observed progress, with concise user updates. Repeated rapid
screenshots, refreshes or identical prompts do not produce better evidence. If
the browser is unavailable, record the actual failure and preserve the complete
prompt; use one supported alternative when evidence suggests it can work.
Return `partial` or `blocked_external` with an exact next action when necessary.

## Compatible project records

These templates and the checker are optional reusable formats. Keep an existing
project's working task-card and receipt format when it carries the needed source,
output and recovery evidence. Recover missing metadata from actual records;
do not repeat valid production just to migrate a format. The checker validates
its own bundle contract, not permission to proceed with other project workflows.

## Return and verify

Preserve the original downloaded files and each intentional revision. A screenshot
is only UI evidence. Record actual submitted prompts separately from drafts.
Return RESULT using [WEB_RESULT.json](../../../templates/WEB_RESULT.json), plus
PROMPTS, REVIEW and STATUS. Reuse an existing candidate when suitable; identify
its source and copy the selected file into the assigned bundle without changing
pixels. Do not generate substitutes merely to satisfy a file count.

The coordinator supplies expected identity/class and checks the local bundle:

```text
python scripts/check_web_handoff.py <bundle>/RESULT.json --root <bundle> --task EXAMPLE-001 --dispatch EXAMPLE-001-r1 --kind design_reference
```

RESULT itself and its referenced files belong inside the bundle root. Paths in
RESULT are relative to that root. Include actual prompts and assets there, not
paths into another producer's output. Record prompt bytes/SHA-256 as well as asset
bytes/SHA-256. Include non-empty `REVIEW.md` and `STATUS.json` at the bundle root;
STATUS must match RESULT's task, dispatch, producer and completed state.
Save outputs, prompts, RESULT and REVIEW first. Persist the final STATUS last,
with `STATUS.status=RESULT.status`. Use `completed` only after those deliverables
and the producer's checks are complete; interrupted work remains non-completed.
The checker is read-only and verifies structure, identity, containment, file
sizes and SHA-256. Exit 0
means a completed bundle passed those checks. It does not decode images, verify
pixel dimensions, source truth, model identity, visual quality, rights, engine
behavior or Owner approval. An unfinished template is not a completed result.
Keep `owner_review=pending` and `engine_status=not_tested` in the producer record;
later acceptance belongs in a separate coordinator/Owner evidence record.

Open the actual output next. Research needs source-backed decisions, not only
links. Images need dimensions/format inspection and visual QA. A color image does
not imply valid normal/roughness/height maps. Concept geometry needs measured
construction and collision tests before it can inform engine acceptance.

Use [material-production.md](material-production.md) to select checks for
repeating textures, atlases and unique surfaces. The optional image inspector
reports actual pixels and Pillow decode observations; it is not a full container
integrity validator. Keep per-criterion deviations and unknowns alongside
production status. Supersede an overbroad acceptance record without erasing its
original files or repeating the completed browser request.

## Absorb and continue

Rewrite transferable lessons into the existing station playbook; keep private
prompts, conversation ids, downloaded files and project dimensions in overlay.
Do not replace the generic station with one World's preferences. Project-specific
generic tool wrappers are not proof that proposed `world_*` tools are implemented.

For a non-Git Unity project, the authorized project writer records the baseline
scene/assets, file hashes, backup path, owned write set and restore route before
mutation. Validate new models/materials in an isolated project-owned scene when
that helps protect the accepted baseline. Reopen saved assets for readback. Keep
visual/structural checks, ClientSim, PCVR and multiplayer evidence separate.

After compaction, recover scope and writer, last confirmed result, artifact paths,
remaining acceptance and one next action from the project handoff. Recheck changed
disk/Editor state; do not replay completed work or reread entire transcripts.
