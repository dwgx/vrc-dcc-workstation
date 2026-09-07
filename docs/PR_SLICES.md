# Public PR slices

English commits. Do not push or open a GitHub PR unless the clone owner asked. Default: land locally, keep the overlay gitignored.

| Slice | Status | Scope | Tests / checks | Keep out |
|---|---|---|---|---|
| **S00-a** | Landed (`9ba91ca`) | Broken relative links; catalog vs default bridge; **playbooks not a named product** | `eval-agent-contract.py`; `query.py`/`refresh.py` require `<avatar>` | Live `maps/<id>/`, `OWNER.md`, `local.json` |
| **S00-b** | Landed | Fail-closed avatar identity and POLICY | `tests/test_policy_identity.py`; wrong name / duplicate / bad schema; Unity compile `NOT_RUN` | Role content, USB packs, first-match mesh fallback |
| **Drop-on-agent** | Landed this tree | English paste block; install questionnaire Q8/Q9; skill YAML refuses foreign-repo auto-apply | `eval-agent-contract.py` (DROP_ON_AGENT + skill `Do not use`) | User-global skill copies; overlay |
| **S00-c** | Landed this tree | Tool allowlist, nonzero MCP errors, request id, JOB lease (file lock, holder required) | `tests/test_s00c_lease_allowlist.py` (fake MCP, LEASE_HELD, concurrent begin, skip_lease tests only) | Upload / Publish APIs; live Editor |
| **S01-a** | Framework this tree | World maps CLI: `init_world` / `world_handshake` / `world_gate` (lease). `world_*` names proposed | `tests/test_s01_world_framework.py` | Installing into a real Worlds project; live `world_*` HTTP |
| **S01-b** | Later (Chat research) | Core / Avatar / World assemblies | Three compile fixtures | Adding Avatar SDK to a Worlds project to make it compile |
| **S01-c** | Later (after authorized Worlds Unity path) | Read-only `world_*` dumps | Wrong Editor, dirty additive scene, no write side effects | Generic `execute_code` |
| **S01-d** | Schema this tree | Evidence fingerprints, STALE, owned plan/apply (`maps/evidence.py`) | `tests/test_s01d_evidence.py` | Bulk content generation; treating Python PASS as in-world |

How to run the loop: [ITERATION.md](ITERATION.md). Do not wait for every catalog URL before the next public slice. Do not treat a research ZIP as a commit.
