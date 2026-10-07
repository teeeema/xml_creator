# OP49 Canonical Import: 166

Validated input: `codex_reports/OP49_P_DS_01/OP49_REAUDIT_REQUIREMENTS.csv`.

Primary-source boundary checks were repeated against `/Users/tema/Documents/Work/Документы_xml/49_ОП.pdf`: PDF page 79 starts Table 10 / MSG.001, page 85 contains Table 10 requirement 35, page 103 starts Table 14 / MSG.006, and page 108 contains Table 14 requirements 32–37. These directly confirm the two ranges missed by the superseded 159-row checkpoint.

- Imported: **166** canonical requirements / **166** unique IDs.
- MSG.001: **35**
- MSG.002: **38**
- MSG.003: **0**
- MSG.004: **2**
- MSG.005: **54**
- MSG.006: **37**
- Missing source text: **0**
- Missing source trace: **0**
- Missing closure criteria: **0**
- Strict `IMPLEMENTED_CONFIRMED`: **0**
- Strict OPEN: **166**
- Canonical source trace complete: **166 / 166**

The re-audit records three source-conflict patterns affecting 35 requirement rows. The migration preserves those conflicts as unresolved evidence and does not select either side by inference.

OP49 audit dependency identifiers are preserved as `AUDIT_DERIVED` recorded-dependency nodes in the dependency graph. The country→currency dependency remains the descriptive `OFFICIAL_MEMBER_STATE_CURRENCY_CODE_MAPPING`; no classifier number or payload is invented.
