# FIX_NOW_CODE FINAL AUDIT

STATUS: PARTIAL_WITH_EXPLICIT_REASONS

FIX_NOW_TOTAL: 178
FIX_NOW_CLOSED_CONFIRMED: 141
FIX_NOW_REMAINING: 37

Remaining: OPEN_CLASSIFIER 22; OPEN_SOURCE_CONFLICT 9; OPEN_EXTERNAL_REGISTRY 4; OPEN_NORMATIVE_AMBIGUITY 2. OPEN_ENGINE / OPEN_EXTERNAL_DATA / OTHER_OPEN: 0.

178 = 141 + 37. Исторический результат 141/178 независимо подтвердился; он не использован как критерий отбора. Построчные результаты: [FIX_NOW_CODE_RESULTS.csv](FIX_NOW_CODE_RESULTS.csv), одна строка на каждый исходный GAP. Отсутствующие данные, конфликты и неоднозначности не выдуманы и не закрыты.

Root-level FIX_NOW_CODE отчёты уже tracked; требуемые новые экземпляры физически созданы в codex_reports.

Дата: 2026-10-05. HEAD: 0d78d9d8523d675ae0dd207f92c2d62ed7c9a8ec. Область: только OP22 / P.SP.02.

## Свежие regression tests

```sh
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q P.SP.02_OP_22/tests -p no:cacheprovider --junitxml=/tmp/op22_report_refresh_tests.xml
PYTHONDONTWRITEBYTECODE=1 python3.13 -m pytest -q -p no:cacheprovider --junitxml=/tmp/op22_report_refresh_full.xml
```

OP22: 3103 passed, 102.97s, exit 0. Full: 3586 passed, 62348 subtests passed, 124.79s, exit 0. Это новые прогоны.

## Метод и границы доказательства

Исходный набор: OP22_GAPS_REVIEWED.csv, op=OP22, review_status=FIX_NOW_CODE. GAP ID — порядковый логический CSV-record, включая заголовок, не физическая строка. Канонический ключ: message/current table/requirement. Диапазоны раскрыты; inherited original source не считается отдельным требованием.

Для каждого CLOSED_CONFIRMED проверены текущие compiled production rule IDs, реализованный DSL, положительные и отрицательные XML regression tests, выполненные в новом прогоне. FIX_NOW_CODE_RESULTS.csv содержит точные test nodes для воспроизведения. Использован существующий production serialize/parse/extract/evaluate pipeline. PASS относится к конкретному требованию; минимальный positive XML не объявлен валидным по всем правилам сообщения. Полные XML покрываются существующими end-to-end regression tests.

Проверены фильтрация повторов, owner-scoped проверки, OR, cardinality после predicate, сравнение экземпляров и типизированные сравнения. Старое название capability не подменяет смысл нормы: AddressKindCode=2 — литерал, не второй адрес. MSG055 сохраняет BankAccountDetails OR PaymentSystemAccountDetails. Исходные XML owner/path сохранены отдельно; production selectors и QName получены из текущих rules/StructureDefinition.

Общий inventory 1609 восстановлен из существующих business_rules/source_refs. Это НЕ новый независимый построчный PDF-аудит всех требований. Для не-FIX строк implemented означает текущую исполнимую coverage без известных partial/open остатков, а не индивидуальную positive/negative сертификацию каждой строки. SAFE_PARTIAL остаётся OPEN. Ссылки на test files открытых GAP не доказывают их закрытие. UNRESOLVED owner не заменён выдуманным XPath.

PDF spot-check физических страниц 519, 520, 537, 577, 760, 776, 795 использован для отдельных source/semantic blockers. Полное независимое перечитывание PDF не заявляется. Исходные причины/source refs сохранены.

Код, tests, YAML, GUI, classifiers не изменялись. Commit/push не выполнялись. Другие OP не пересчитаны. Предсуществующее изменение eaeu_xml/.DS_Store не относится к этой задаче.

## Повторная арифметическая сверка

Из корня репозитория:

```sh
PYTHONDONTWRITEBYTECODE=1 python3.13 - <<'PY'
import csv
from pathlib import Path
p=Path('codex_reports')
fix=list(csv.DictReader((p/'FIX_NOW_CODE_RESULTS.csv').open()))
gaps=[r for r in csv.DictReader((p/'FINAL_DELIVERY_GAPS.csv').open()) if r['op']=='OP22']
assert len(fix)==len({r['gap_id'] for r in fix})==178
closed={r['canonical_requirement_id'] for r in fix if r['current_status']=='CLOSED_CONFIRMED'}
remaining={r['canonical_requirement_id'] for r in gaps}
assert len(closed)==141 and len(remaining)==len(gaps)==346
assert closed.isdisjoint(remaining)
assert all(r['canonical_requirement_id'] in remaining for r in fix if r['current_status']!='CLOSED_CONFIRMED')
for name in ('FINAL_DELIVERY_MESSAGE_MATRIX.csv','FINAL_DELIVERY_TRANSACTION_MATRIX.csv'):
    rows=[r for r in csv.DictReader((p/name).open()) if r['op']=='OP22']
    total='expanded_requirements' if 'expanded_requirements' in rows[0] else 'normative_requirements'
    assert all(int(r[total])==int(r['implemented_requirements'])+int(r['remaining_gaps']) for r in rows)
    assert sum(int(r[total]) for r in rows)==1609
    assert sum(int(r['implemented_requirements']) for r in rows)==1263
    assert sum(int(r['remaining_gaps']) for r in rows)==346
print('PASS')
PY
```

Production rule IDs и positive/negative pytest nodes каждой закрытой строки дополнительно сверяются с текущими rule/test files; команды выше повторяют исполнение.
