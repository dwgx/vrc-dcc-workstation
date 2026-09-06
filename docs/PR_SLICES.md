# Public PR slices

English commits. Do not push or open a GitHub PR unless the clone owner asked. Default: land locally, keep the overlay gitignored.

Each slice should include a failing fixture first (when the change is code), then the fix, then docs/i18n that the slice actually touches. Offline tests are `PASS`; Unity compile/register without an Editor is `NOT_RUN`.

| Slice | Scope | Tests / checks | Keep out |
|---|---|---|---|
| **S00-a** | Broken relative links; catalog vs default bridge; **playbooks not a named product** | `eval-agent-contract.py`; `query.py`/`refresh.py` require `<avatar>` | Live `maps/<id>/`, `OWNER.md`, `local.json` |
| **S00-b** | Fail-closed avatar/world identity and POLICY | Wrong name / duplicate name / bad schema | Role content, USB packs |
| **S00-c** | Tool allowlist, nonzero tool errors, request id, JOB lease | Fake MCP notify-before-result; timeout; cross-domain | Upload / Publish APIs |
| **S01-a** | `skills/vrc-world`, world profile template, routing | Avatar job fixtures still hit `vrc-dcc` | Installing into a real Worlds project |
| **S01-b** | SDK-independent Core + Avatar/World assemblies | Three compile fixtures | Adding Avatar SDK to a Worlds project to make it compile |
| **S01-c** | Read-only `world_*` dumps | Wrong Editor, dirty additive scene, no write side effects | Generic `execute_code` |
| **S01-d** | Evidence fingerprints, STALE, owned plan/apply | Replay, lost lease, shared-asset consumers | Bulk content generation |

Do not wait for every catalog URL before the first public slice. Do not treat a research ZIP as a commit.
