# Research executor brief

Copy into a private task pack and fill from the owner's request. Use when a
separate researcher will return evidence to a coordinator. This is an optional
companion to [WEB_TASK.md](WEB_TASK.md), not a scheduler or a new agent policy.
Reuse an existing project format when it carries the same useful information.
When copying, resolve the links below against this station root or replace them
with the actual local reference paths in the filled brief.

## Commission

- Coordinator task and return channel: FILL with the actual task identity.
- Executor: FILL from the actual runtime; a prompt does not select its model.
- Task / dispatch: FILL. An uncertain-send recovery retains its dispatch.
- Owner goal and decision the research should change: FILL.
- Seed sources and already-consumed evidence: FILL with URLs, revisions and paths.
- Open questions, in priority order: FILL.
- Assigned output directory and write set: FILL.
- Authorized browser/CLI actions and requested model settings: FILL from the
  owner's existing authorization, without inventing a new permission round.
- Completion for this assignment: FILL with concrete evidence and a next action.

## Work

1. Read the current brief and relevant completed result before searching again.
   Identify the coordinator, other active writers and the source snapshots.
   Recover a missing decision through a bounded history lookup when necessary.
   Write only the assigned output set. If another producer owns that assignment,
   coordinate before taking it over; do not overwrite its queue or recovery files.
2. Build a small source map. Distinguish authored article bodies, code, video
   metadata, transcripts, search pages and archive pointers. A catalog record
   is a lead until its relevant content has actually been inspected.
3. Read the sources that can change the stated decision. Follow original docs,
   code and author reports; keep independent corroboration and counterexamples.
   Expand to related sources as the question requires. Coverage is question-led;
   an initial batch size is not a universal research limit.
4. Use a web analyst for synthesis or unresolved questions when useful. Preserve
   the exact submitted prompt, source context, requested and visible model
   settings, conversation URL and last confirmed action. Follow
   [web-handoff.md](../skills/vrc-dcc/references/web-handoff.md) for browser
   submission, recovery and result files. Reopen an uncertain send before retrying.
5. Verify consequential claims from the reply against the original source. Keep
   static source findings, runtime observations and proposals distinguishable.
   If one route fails, preserve its state, use another already-authorized route
   when useful, and continue independent questions. Record an unfinished result
   honestly; process exit success alone does not establish task completion.
6. Return useful mechanisms with prerequisites, an example, limitations, a
   suggested station file/tool change and the check that would justify adoption.
   Preserve useful existing capabilities; a limitation of one project or adapter
   does not become a universal ban on the technique.

## Return

Keep a compact source ledger, using an existing format or a Markdown table:

| Source / original-author group | Revision, published date and read date | Content actually read + locator | Claim and applicable versions | Conflicts / unresolved points | Suggested use |
|---|---|---|---|---|---|
| URL or local source file | Unknown is explicit | Body, code, metadata, transcript or pointer | What this evidence supports | What still needs checking | Candidate improvement |

The return includes:

- Findings organized by the coordinator's questions, with source locators.
- A coverage note: sources read, leads only, access failures and consequential gaps.
- A few actionable proposals, with local/runtime checks still needed.
- Exact prompts and the original web reply when a web analyst was used.
- A resumable status and one next action. Save outputs before final status.

For browser work, use the existing WEB_TASK/WEB_RESULT bundle or its compatible
project equivalent. When using WEB_RESULT, use its `running`, `completed`,
`partial` or `blocked_external` status values. Save outputs, RESULT and REVIEW
before final STATUS, with `STATUS.status = RESULT.status`; `completed` means the
assigned deliverables and producer checks are finished. Keep raw local histories,
private task IDs and licensed assets
in the private pack; publish only appropriate source references and rewritten
methods. Research deliverables can be complete while adoption remains pending.

If the owner authorized cross-task reporting and a supported messaging tool is
available, send one completion or actionable-blocker message to the named
coordinator with task/dispatch, local result paths, key findings and remaining
checks. Record the dispatch and confirmed or uncertain delivery in the recovery
record; inspect an uncertain delivery before retrying. Do not send the full archive.
If delivery fails, leave a usable file
handoff and say that delivery was not confirmed. Avoid reciprocal wait loops.

The coordinator reads the evidence, accepts/revises/rejects the proposals in its
own record, and performs any implementation within its authorized project scope.
The producer's completion is not coordinator, engine or owner acceptance.
Further batches follow the current owner direction; recurring work requires an
explicit scheduling request.
