# Read-only diagnosis, 2026-10-23

OP22 → P.SP.02.PRC.008 → P.SP.02.TRN.003 → P.SP.02.MSG.004 → T38 REQ2/3 → R.IP.SP.02.002 → ipcdo:TrademarkApplicationDetails/ipsdo:IPDocKindCode and IPDocKindName.

Original PDF physical pp531–534: T38 starts p531; REQ2/3 p532; REQ5 and inherited6–29 plus attached document REQ30 p533. RTF section49/Table38 agrees. Decision92 p13 and Decision148 p3 independently confirm07320 for the interested-party Article8 document. Exact source excerpts/hashes: sources.json. Local snapshot lacks07320; no executable REQ2/3 and no effective Code/Name policy. before.json records actual get_form, GuiController controls, scoped namespace-aware XML and validator false accepts.

Expected: Code FIXED07320 readonly; direct Name FORBIDDEN; raw missing/wrong/both rejected. Actual before: editable Code/Name, no policy; raw wrong/missing/Code+Name accepted. Root cause belongs to MSG004 mapping and stale classifier subset, not shared evaluator.

REQ3 fallback depends on classifier entry absence, not missing Code in XML. With confirmed07320 it is inactive. REQ30 separately requires Name on nested AccompanyingDocumentsDetails; do not forbid all Name QNames globally. REQ4 external Commission resource check remains partial and is outside this correction.

Read-only product audit completed before correction; baseline hashes recorded. Normative originals unchanged. GUI proof means real form/controller state, not a manually observed desktop screenshot.
