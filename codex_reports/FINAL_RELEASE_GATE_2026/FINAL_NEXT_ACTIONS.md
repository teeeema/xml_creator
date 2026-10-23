# FINAL NEXT ACTIONS

1. Run the project's final KB synchronization against the exact current workspace state without discarding any existing user changes.
2. Refresh `knowledge_base/data/project_state/current.json` and requirement `project_state` links/evidence so they reference the same production/test/engine state that will be gated.
3. Revalidate canonical scope = 2894 and source freshness; preserve unresolved normative/classifier/external blockers as blockers rather than guessing.
4. Record explicit completion evidence: `KB_FINAL_SYNC = COMPLETE` and `READY_FOR_FINAL_GATE = YES`.
5. Re-run the independent final release gate. Only then execute the five gates and the six regression suites.
