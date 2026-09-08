# Evolve a project with its source template

Use when the owner requests an update, a relevant upstream fix appears during
current work, or an authorized project milestone calls for checking its methods.
This is an on-demand maintenance route for World and Avatar projects. It does
not add a scheduler, require a check on every startup, or replace a project's
existing agents and records.

## Keep three versions distinguishable

- **Baseline:** the source revision previously reconciled with a particular
  local file. Different copied templates can have different baselines.
- **Candidate:** the source commit inspected this time. Fetching or reading it
  does not mean the project has integrated it.
- **Local:** the project's current implementation, including its agent's edits.
  Local improvements remain useful even when the source has changed.

Record the source repository and actual branch. Do not assume every source uses
`master` or `main`. Inspect the configured remotes, then query the chosen source:

```sh
git remote -v
git ls-remote --symref origin HEAD
git fetch origin
```

These commands are examples for a clone whose source is `origin`; a fork may
use a separate `upstream` remote. Fetch updates local remote-tracking refs, not
the working files. Resolve the selected candidate to a commit before reviewing.
See [Git remotes](https://git-scm.com/docs/git-remote) and
[Git diff](https://git-scm.com/docs/git-diff).

## Choose the consumer's actual layout

| Layout | Useful update method |
|---|---|
| Git clone or fork | Compare source baseline, candidate and the current working files; merge on an owned branch/worktree and retain local commits. |
| Copied templates in a Git or non-Git project | Map each source file to its local target and recorded source baseline; adapt selected changes in the project writer's scope. |
| Agent reads a file by reference | Record the revision/hash actually consumed by the task. A changed file on disk does not refresh an already loaded prompt. |
| Generated assets or completed task cards | Preserve the original inputs/receipt. Create a new revision for changed behavior; updating a blank template does not migrate completed work. |

Recover writer ownership and Git status, or the project's existing backup method
when it has no Git. Independent source research may continue beside production.
An active writer can integrate the result at its next suitable boundary; do not
have two agents overwrite the same queue, scene, contract or configuration.

## Optional read-only comparison

The stdlib + Git helper [compare_upstream.py](../../../scripts/compare_upstream.py)
reads already available Git objects and selected local files. It does not fetch,
merge, invoke DCC tools, run external diff/clean filters, or update adoption
records. It outputs hashes and classifications, not file contents.

For a clone, replace `BASE_COMMIT` with its recorded source baseline and choose
the actual fetched candidate ref:

```sh
python scripts/compare_upstream.py --repo . --base BASE_COMMIT --upstream origin/main --path templates --path skills/vrc-world
```

For copied/adapted files, copy
[UPSTREAM_FILES.example.json](../../../templates/UPSTREAM_FILES.example.json)
into the project's existing private records and fill the paths. `source_path`
is relative to the source repo; `target_path` is relative to `--local-root`.
Each `base_commit` is its recorded full Git hash, or `null` when unknown:

```sh
python scripts/compare_upstream.py --repo ../vrc-dcc-workstation --upstream origin/main --local-root ../my-world --manifest ../my-world/.production/upstream-files.json
```

The mapped project needs no Git repository. Neither layout needs a new global
registry. `--output` writes a new JSON receipt and refuses to replace an existing
file. Default comparison uses exact bytes; `--ignore-crlf` optionally treats
CRLF and LF as equivalent for valid UTF-8 text without NUL bytes. Raw hashes and
the selected comparison policy remain in the receipt. Use that option only when
line endings are a checkout difference rather than a meaningful local change.

| Result | Meaning and next action |
|---|---|
| `unchanged` | Selected contents match baseline and candidate. |
| `upstream_changed` | Local contents match baseline; inspect the upstream addition, modification or deletion and its dependencies. |
| `local_changed` | Upstream matches baseline; retain the local improvement and consider whether it is reusable. |
| `converged` | Both sides now have matching contents. Check behavior before recording integration. |
| `both_changed` | Both differ from baseline and each other. Review both deltas; this does not assert a textual conflict. |
| `baseline_unknown` | Recover the original source revision or compare manually. Do not assume a local customization is untouched upstream content. |
| `manual_review` | Special entries, unstable reads or other unsupported cases need inspection. |

The report is content comparison, not a merge/compatibility verdict. Read its
review reasons and ancestor information. Renames appear as old/new paths;
permission semantics, expanded LFS assets and runtime compatibility require
separate review. A valid report exits `0` even when it contains review items;
input/Git errors exit `2`. A source checkout lacking required objects needs a
separate explicit fetch before retrying.

## Integrate and verify a useful change

1. Read the relevant upstream commits and both source/local deltas. Include
   companion scripts, schemas, tests and translated docs when they are dependencies.
2. Choose **adopt**, **adapt**, **defer** or **keep local**, with a short reason.
   An upstream simplification does not justify dropping a working local capability.
3. Work on an owned branch/worktree or the project's established backup. Merge
   or edit the selected changes there; ordinary authorized improvements do not
   need another approval ceremony. Keep private assets and machine configuration
   in their existing overlay.
4. Run checks appropriate to the changed behavior. A prompt/schema update needs
   a consumer example; a Blender/Unity change needs the relevant engine readback.
   A clean text merge or successful source CI does not validate another project.
5. Review the result independently when material. Record the actual local commit
   or file hashes, checks and remaining runtime work. Advance the baseline only
   for files whose candidate changes have been reconciled. If some hunks remain
   unreviewed, keep that file's old baseline and record partial adoption.

Use existing project records, or [UPSTREAM_UPDATE.md](../../../templates/UPSTREAM_UPDATE.md).
Keep `last checked` separate from `integrated`. Updating one template must not
mark a whole repository version integrated. Preserve completed cards and record
which revised prompt the next producer actually consumes.

`bootstrap.ps1 -Apply` initializes an installation and missing configuration; it
is not an upgrade merge. Existing custom MCP needs an intentional reviewed edit.
A runtime skill copy likewise needs a content/revision comparison: existence or
newer timestamps alone do not establish synchronization. Follow the chosen
project-local distribution convention; do not bulk overwrite runtime copies.

## Let local improvements return to the source

When a project agent solves a reusable problem, send its coordinator a bounded
return: source baseline, problem/trigger, portable patch or proposal, changed
paths, reproduction and actual checks. Separate private project geometry,
credentials, task IDs and owner-specific policy from the general mechanism.

The source maintainer reviews that delta, adapts it to the public skeleton and
publishes under the owner's existing remote/authorization convention. A foreign
clone follows its own fork/contribution arrangement; it does not automatically
push to the template author's repository. The return can use the project's
existing handoff/PR, [RESEARCH_EXECUTOR.md](../../../templates/RESEARCH_EXECUTOR.md)
or the feedback section of `UPSTREAM_UPDATE.md`.

After landing, return the source commit and validation to the originating
project. That project reconciles the result with its local version, avoiding a
second application of a fix it already contains. Other consumers discover it
when relevant to their work. Research collected, source published and consumer
validated are three distinct milestones.
