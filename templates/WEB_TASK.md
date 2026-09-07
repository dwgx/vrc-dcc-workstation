# Web task (copy to a gitignored task pack)

The coordinator fills this card. The producer follows the authorized task and
writes the assigned result bundle. This card does not select a runtime model or
grant permissions beyond the user's task. Workflow:
[web-handoff.md](../skills/vrc-dcc/references/web-handoff.md).

## Assignment

```yaml
task_id: EXAMPLE-001
dispatch_id: EXAMPLE-001-r1
artifact_class: research | design_reference | base_color_candidate | model_reference
coordinator: FILL
producer: FILL
project_root: FILL
bundle_root: FILL
task_file: FILL
write_set: [FILL]
authorized_actions: [FILL]
requested_web_model: FILL
requested_reasoning: FILL
state: ready
depends_on: []
```

State the goal and the decision this result will enable. List required outputs
by name, dependencies and what satisfies them. Separate ready items from held
items. A producer must not re-run a completed task because the queue is old.

## Source and scope

- Current handoff and source evidence: exact paths/sections or primary URLs.
- Owner decisions: short attributed excerpts or paraphrases, with date/location.
- Candidate assumptions: label these separately; do not call them Owner approval.
- Necessary references to upload/read: exact files only.
- Write set: only the bundle root; no task/queue/Editor/asset-shelf changes.
- Conversation: assigned URL or permission to create one for this task.
- Allowed sends/uploads/downloads: reuse the user's existing authorization.

Record the task-relevant actions and the user's instruction that authorizes them.
An incomplete card can be completed from known session context without asking
again. If target, writer or permission is unknown, resolve only that uncertainty
before the dependent action; do not treat a template placeholder as permission.

## Complete prompt

Write the actual prompt here, including goal, relevant context, requested output,
constraints, and quality criteria. Do not send the entire project/history pack.
For research, ask for checked primary sources, dates/versions, recommended choices,
and unresolved uncertainty. For images, state their intended use and review criteria.

## Execution and revisions

Observe current browser UI/tool support. Record requested and visible model values
separately. Reuse the task's conversation after timeout/reset; confirm whether a
send occurred before sending again. Preserve revisions and explain specific changes.
Do not claim a backend model that the UI does not reveal.

Initialize STATUS before sending:

```json
{
  "task_id": "EXAMPLE-001",
  "dispatch_id": "EXAMPLE-001-r1",
  "producer_session": "FILL",
  "task_file": "FILL",
  "bundle_root": "FILL",
  "artifact_class": "FILL",
  "write_set": ["FILL"],
  "status": "running",
  "stage": "prepared",
  "chat_url": null,
  "last_confirmed_action": "Task read; prompt has not been sent",
  "next_action": "Observe assigned browser conversation",
  "updated_at": "FILL"
}
```

Update the stage (`prepared`, `sending`, `waiting`, `downloaded`, `reviewed`) and
last confirmed action as work advances. Preserve uncertainty after a failed call.
This file does not implement a concurrent lease; do not claim another active
producer's assignment.

## Deliverables

- `PROMPTS.md`: exact submitted prompts, references and revisions; distinguish drafts.
- `assets/`: original downloads or research reports, preserving previous revisions.
- `RESULT.json`: fill [WEB_RESULT.json](WEB_RESULT.json); all paths bundle-relative.
  Record `actual_prompts_bytes` / `actual_prompts_sha256` and each asset's bytes/hash.
- `REVIEW.md`: findings, source/visual checks, known issues, recommendation and remaining checks.
- `STATUS.json`: completed/partial/blocked_external, conversation URL and next action.

Keep RESULT, REVIEW and STATUS inside the bundle. A completed STATUS must agree
with RESULT's task/dispatch/producer/completed state; stale recovery records cannot
close a new assignment.
Save outputs, prompts, RESULT and REVIEW before persisting the final STATUS.
Set `STATUS.status=RESULT.status` last; use `completed` only when the producer's
deliverables and checks are finished. Keep partial/blocked work explicit.

Expected checker identity is task/dispatch/class from this coordinator card, not
values copied back from the producer's RESULT. Keep Owner and engine acceptance
pending in the producer record. The coordinator checks file integrity, then actual
content, and records acceptance separately. Image dimensions/format, source accuracy,
tiling, PBR channels, mesh readiness and PCVR are not certified by a hash check.
