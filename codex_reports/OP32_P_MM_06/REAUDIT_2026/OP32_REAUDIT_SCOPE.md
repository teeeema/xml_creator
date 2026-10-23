# OP32 / P.MM.06 RE-AUDIT SCOPE RECONSTRUCTION

**Date**: 2026-10-07  
**Process**: P.MM.06 (v1.1.0) — Формирование, ведение и использование единого реестра медицинских изделий, зарегистрированных в рамках ЕАЭС  
**Primary Normative Source**: `/Users/tema/Documents/Work/Документы_xml/32_ОП.pdf` (Решение Коллегии ЕЭК от 30.08.2016 № 92 в ред. № 120 от 19.09.2017 и № 19 от 28.02.2023, 212 страниц)  
**Audit Mode**: READ ONLY, Full Independent Re-audit with 6 Multi-Agent Auditors (Subagents A, B, C, D, E, F)

---

## 1. Executive Summary: Scope Reconstructed vs Baseline

| Scope Dimension | Normative Primary Source (32_ОП.pdf) | Historical Package Catalog | Status / Verification Note |
|---|---|---|---|
| **Process Definition** | 1 (`P.MM.06`, v1.1.0) | 1 (`P.MM.06`) | CONFIRMED v1.1.0 (PDF p. 5, п. 6) |
| **Actors (ACT)** | **7** (`P.ACT.001`, `P.MM.06.ACT.001`–`006`) | 7 | CONFIRMED in Table 1 (PDF pp. 5–7) |
| **Procedures (PRC)** | **15** (`PRC.001`–`PRC.015`) | 15 | CONFIRMED in Tables 2–7 (PDF pp. 8–20) |
| **Operations (OPR)** | **46** (`OPR.001`–`OPR.046`) | 44 | **GAP IDENTIFIED**: Package omits `OPR.007` and `OPR.008` (internal EEC Commission publishing operations in PRC.002, PDF pp. 28–32) |
| **Transactions (TRN)** | **15** (`TRN.001`–`TRN.015`) | 15 | CONFIRMED: 7 in Doc 2 + 8 in Doc 3 |
| **Messages (MSG)** | **24** (`MSG.001`–`MSG.024`) | 24 | CONFIRMED: 13 in Doc 2 + 11 in Doc 3 |
| **Document Structures** | **7** (`R.006`, `R.007`, `R.HC.MM.06.001`–`005`) | 7 | CONFIRMED in Document 4 (PDF pp. 158–207) |
| **Normative Requirement Tables** | **14 tables** (Tables 13–25, Table 16 duplicated) | 14 tables | CONFIRMED in Document 2 & Document 3 Section IX |
| **Raw Normative Table Rows** | **162 rows** | Historical miscounted 178 | CONFIRMED: Real PDF rows = 162 |
| **Atomic Business Requirements** | **170 requirements** | Historical claimed 170 | CONFIRMED: 162 raw rows + 8 splits from 6 compound rows = 170 |

---

## 2. Explanation of Row Count Arithmetic & Discrepancies

### A. The 178 Historical Myth
Older extraction attempts reported 178 requirements. This was proven to be caused by a regex boundary parser defect:
- At the end of Document 2 (Table 16, p. 117, MSG.012), the table has only 2 rows. The parser crossed the document boundary and captured numbered paragraphs 1–9 of Document 3 as rows (+9 phantom rows).
- At the end of Document 3 (Table 25, p. 157, MSG.024), the table has only 1 row. The parser crossed into Document 4 and captured paragraphs 1–7 as rows (+7 phantom rows).
- $162 + 9 + 7 = 178$. This error was previously identified and eliminated.

### B. The 162 vs 170 Atomization
There are physically **162 rows** across the 14 tables in Section IX. Exactly 6 rows combine distinct, independent assertions that must be split into separate rules:
1. **Table 13, Row 24 (MSG.001)**: Uniqueness check against 3 distinct external registers (medical products, medicinal products, dietary supplements) -> **+2 requirements**.
2. **Table 14, Row 5 (MSG.002)**: Mandates both `csdo:DocValidityDate` AND `hcsdo:MedicalProductRegistrationCertificateStatusCode` -> **+1 requirement**.
3. **Table 14, Row 40 (MSG.002)**: Mandates `ccdo:CommunicationDetails` presence AND channel code equals "телефон" -> **+1 requirement**.
4. **Table 14, Row 44 (MSG.002)**: Same 3-registry uniqueness check -> **+2 requirements**.
5. **Table 14, Row 45 (MSG.002)**: Mandates `csdo:UnifiedCountryCode` presence AND code belongs to EAEU member state -> **+1 requirement**.
6. **Table 17, Row 7 (MSG.015)**: Mandates `hcsdo:PdfBinaryText` presence AND content verification -> **+1 requirement**.

Total atomic requirements: $162 + 8 = 170$.\n