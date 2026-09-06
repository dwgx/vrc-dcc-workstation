# Public PR slices

English commits. Do not push or open a GitHub PR unless the clone owner asked. Default: land locally, keep the overlay gitignored.

| Slice | Status | Scope | Tests / checks | Keep out |
|---|---|---|---|---|
| **S00-a** | Landed (`9ba91ca`) | Broken relative links; catalog vs default bridge; **playbooks not a named product** | `eval-agent-contract.py`; `query.py`/`refresh.py` require `<avatar>` | Live `maps/<id>/`, `OWNER.md`, `local.json` |
| **S00-b** | Landed | Fail-closed avatar identity and POLICY | `tests/test_policy_identity.py`; wrong name / duplicate / bad schema; Unity compile `NOT_RUN` | Role content, USB packs, first-match mesh fallback |
| **S00-c** | Later | Tool allowlist, nonzero tool errors, request id, JOB lease | Fake MCP notify-before-result; timeout; cross-domain | Upload / Publish APIs |
| **S01-a** | Docs draft | `skills/vrc-world`, world profile template, routing | Avatar job fixtures still hit `vrc-dcc` | Installing into a real Worlds project |
| **S01-b** | Later | SDK-independent Core + Avatar/World assemblies | Three compile fixtures | Adding Avatar SDK to a Worlds project to make it compile |
| **S01-c** | Later | Read-only `world_*` dumps | Wrong Editor, dirty additive scene, no write side effects | Generic `execute_code` |
| **S01-d** | Later | Evidence fingerprints, STALE, owned plan/apply | Replay, lost lease, shared-asset consumers | Bulk content generation |

How to run the loop: [ITERATION.md](ITERATION.md). Do not wait for every catalog URL before the next public slice. Do not treat a research ZIP as a commit.
