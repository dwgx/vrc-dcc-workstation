# Public PR slices

English commits. Do not push or open a GitHub PR unless the clone owner asked. Default: land locally, keep the overlay gitignored. Existing authorization to update the owner's GitHub repository includes normal commits and pushes within that scope.

| Slice | Status | Scope | Tests / checks | Keep out |
|---|---|---|---|---|
| **S00-a** | Landed (`9ba91ca`) | Broken relative links; catalog vs default bridge; **playbooks not a named product** | `eval-agent-contract.py`; `query.py`/`refresh.py` require `<avatar>` | Live `maps/<id>/`, `OWNER.md`, `local.json` |
| **S00-b** | Landed | Fail-closed avatar identity and POLICY | `tests/test_policy_identity.py`; wrong name / duplicate / bad schema; Unity compile `NOT_RUN` | Role content, USB packs, first-match mesh fallback |
| **Drop-on-agent** | Landed this tree | English paste block; install questionnaire Q8/Q9; skill YAML refuses foreign-repo auto-apply | `eval-agent-contract.py` (DROP_ON_AGENT + skill `Do not use`) | User-global skill copies; overlay |
| **S00-c** | Landed this tree | Tool allowlist, nonzero MCP errors, request id, JOB lease (file lock, holder required) | `tests/test_s00c_lease_allowlist.py` (fake MCP, LEASE_HELD, concurrent begin, skip_lease tests only) | Upload / Publish APIs; live Editor |
| **S01-a** | Framework this tree | World maps CLI: `init_world` / `world_handshake` / `world_gate` (lease). `world_*` names proposed; prefix is not callable | `tests/test_s01_world_framework.py` (`world_*` → not implemented) | Installing into a real Worlds project; live `world_*` HTTP |
| **S01-b** | Proposed — compile evidence required | Split installable Core / Avatar / World packages and Editor assemblies. Keep `com.vrc-dcc.tools` and `VrcDcc.Tools.Editor` as the Avatar adapter. No SDK types in Core; no Avatar SDK / MA / NDMF in World | Core-only, Avatar-only and Worlds-only Unity 2022.3 fixtures; cold compile; domain reload; named-tool discovery. Record PASS / NOT_RUN | Mixed SDK projects; live-test assets; a meta-package that installs both adapters |
| **S01-c** | Proposed — after S01-b and an authorized Worlds project | Bounded, read-only `world_probe` only. Exact Editor/project/scene identity, JOB lease, implemented-tool allowlist | Wrong/missing Editor; two-Editor routing; dirty additive / unsaved / Prefab Stage; ambiguous descriptors; no project writes | `world_scene_dump` / `world_udon_inventory`; generic execution; auto-save/compile/Play/Publish |
| **S01-d** | Schema this tree | Evidence fingerprints, STALE, `mutation_revision`, owned plan/apply (`maps/evidence.py`). Not a complete freshness engine | `tests/test_s01d_evidence.py` (timestamp-wash → STALE_MUTATED) | Bulk content generation; treating Python PASS as in-world |
| **World production** | Workflow and CLI this tree | Installed provider tools; optional station maps; continuous World slices without Avatar SKU quotas; reset preserves mutation history | World CLI lifecycle, competing holder, legacy overlay and revision regressions | Claiming offline checks prove Editor or runtime behavior |
| **Web handoff** | This tree | Optional task/dispatch receipts, original prompt/output hashes and recoverable send state | `tests/test_web_handoff.py` | Private conversations, generated assets, forcing existing projects to migrate receipts |
| **Chat absorb (2026-09-07)** | Landed this tree | Rewritten two-Editor / three-package / unimplemented `world_*` / STALE matrix rules. Zip and Chat JSON stay overlay | allowlist + evidence tests; `eval-agent-contract.py` | Committing the zip, 900KB JSON, or live `world_probe` C# |

S01-b/c are milestones for the custom station adapter. They do not delay production through [installed World tools](WORLD_PRODUCTION.md).

How to run the loop: [ITERATION.md](ITERATION.md). Do not wait for every catalog URL before the next public slice. Do not treat a research ZIP as a commit.
