# P.MM.06 — нормативный audit структур (исправленный)

Источник: только `32_ОП.pdf`. `R.006`, `R.007`, MessageRules и production-файлы не затрагивались.

## Метод

Нормативная строка таблицы — **PROVEN structural node**, если PDF содержит её иерархический номер, русское имя, описание, ID элемента модели, тип и множественность. Отсутствие XML local name не отменяет этот узел. `local_name` и `qname` оставлены `null` / `MISSING_EVIDENCE`: таблицы 10, 13, 16, 19 и 22 не содержат локальных XML names.

## Summary

| Structure | Таблица / страницы | Proved structural nodes | Numeric rows | `*.n` rows | Root / version |
| --- | --- | ---: | ---: | ---: | --- |
| `R.HC.MM.06.001` | 10 / 169–188 | 116 | 65 | 51 | `MedicalProductRegistrationDetails` / `1.1.0` |
| `R.HC.MM.06.002` | 13 / 189–193 | 19 | 19 | 0 | `MedicalProductRegistrationExpertReportDetails` / `1.1.0` |
| `R.HC.MM.06.003` | 16 / 194–201 | 25 | 25 | 0 | `MedicalProductRegistrationDocContentDetails` / `1.1.0` |
| `R.HC.MM.06.004` | 19 / 202–204 | 9 | 9 | 0 | `MedicalProductRegistrationNumberRequestDetails` / `1.1.0` |
| `R.HC.MM.06.005` | 22 / 205–208 | 17 | 17 | 0 | `MedicalProductCodeTransformationDetails` / `1.1.0` |

## Proven hierarchy and namespaces

- `a.b.c` имеет parent `a.b`; `a.b` имеет parent `a`. Это доказанная hierarchy реквизитов.
- В `.001` строки `*.n` также являются доказанными узлами, но их абсолютный `parent_row_number` не выражен самой нумерацией: для него `MISSING_EVIDENCE`.
- XML hierarchy status всех пяти структур: `PARTIAL`: hierarchy реквизитов доказана; XML local names, QName и paths не доказаны.
- Imports во всех структурах: `ccdo = urn:EEC:M:ComplexDataObjects:vX.X.X`; `hccdo = urn:EEC:M:HC:ComplexDataObjects:vZ.Z.Z`; `hcsdo = urn:EEC:M:HC:SimpleDataObjects:vZ.Z.Z`; `csdo = urn:EEC:M:SimpleDataObjects:vX.X.X`. Placeholders сохранены буквально.

| Code | Namespace | XSD |
| --- | --- | --- |
| `.001` | `urn:EEC:R:HC:MM:06:MedicalProductRegistrationDetails:v1.1.0` | `EEC_R_HC_MM_06_MedicalProductRegistrationDetails_v1.1.0.xsd` |
| `.002` | `urn:EEC:R:HC:MM:06:MedicalProductRegistrationExpertReportDetails:v1.1.0` | `EEC_R_HC_MM_06_MedicalProductRegistrationExpertReportDetails_v1.1.0.xsd` |
| `.003` | `urn:EEC:R:HC:MM:06:MedicalProductRegistrationDocContentDetails:v1.1.0` | `EEC_R_HC_MM_06_MedicalProductRegistrationDocContentDetails_v1.1.0.xsd` |
| `.004` | `urn:EEC:R:HC:MM:06:MedicalProductRegistrationNumberRequestDetails:v1.1.0` | `EEC_R_HC_MM_06_MedicalProductRegistrationNumberRequestDetails_v1.1.0.xsd` |
| `.005` | `urn:EEC:R:HC:MM:06:MedicalProductCodeTransformationDetails:v1.1.0` | `EEC_R_HC_MM_06_MedicalProductCodeTransformationDetails_v1.1.0.xsd` |

## Attributes, special content, integrity

PDF explicitly mentions attributes including `codeListId`, `codeListVersionId` and `media`; they are attributes, not child elements. Their owner remains `MISSING_EVIDENCE` without an XML-name mapping. `.003` contains a binary-document field and an arbitrary embedded XML document; the latter permits arbitrary element / any namespace / validation always performed (PDF стр. 201, таблица 16, row `5.13.1`).

No duplicate explicit row numbers or numeric orphan rows were found. `*.n` is normative relative numbering, not a gap. XML local names, QName, XML paths and attribute ownership are `MISSING_EVIDENCE`. Production files changed: **NO**.
