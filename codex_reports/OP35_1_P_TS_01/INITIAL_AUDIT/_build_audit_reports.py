import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/Users/tema/Documents/Work/xml_creator")
OUT = ROOT / "codex_reports/OP35_1_P_TS_01/INITIAL_AUDIT"
LAYOUT = Path("/tmp/op35_layout_all.txt")
SOURCE_FILE = "35.1 ОП.pdf"

text = LAYOUT.read_text(encoding="utf-8")

structures = {
    "R.004": ("Таблица 4", "13. Описание структуры", 4, 42),
    "R.006": ("Таблица 7", "16. Описание структуры", 7, 10),
    "R.007": ("Таблица 10", "2. Структуры электронных документов", 10, 11),
    "R.TR.TS.01.001": ("Таблица 13", "22. Описание структуры", 13, 307),
    "R.TR.TS.01.002": ("Таблица 16", "УТВЕРЖДЕН", 16, 19),
}

structure_messages = {
    "R.004": "SHARED_COMPONENT_NO_DIRECT_MESSAGE",
    "R.006": "P.TS.01.MSG.003|P.TS.01.MSG.012",
    "R.007": "P.TS.01.MSG.002|P.TS.01.MSG.008|P.TS.01.MSG.009",
    "R.TR.TS.01.001": "P.TS.01.MSG.001|P.TS.01.MSG.007|P.TS.01.MSG.011|P.TS.01.MSG.014",
    "R.TR.TS.01.002": "P.TS.01.MSG.010|P.TS.01.MSG.013",
}

row_pat = re.compile(
    r"(?m)^\s*((?:\d+(?:\.\d+)*\.|\*\.\d+(?:\.\d+)*\.|[абвгд]\)))\s+(.+)$"
)
page_pat = re.compile(r"===== PDF_PAGE (\d+) =====")
prefixes = "bdt|ccdo|csdo|trcdo|trsdo"


def page_at(pos: int) -> int | None:
    matches = list(page_pat.finditer(text, 0, pos + 1))
    return int(matches[-1].group(1)) if matches else None


def normalize_space(value: str) -> str:
    return " ".join(value.split())


def first_cell(line: str) -> str:
    if line.startswith("===== PDF_PAGE") or not line.strip():
        return ""
    first_nonspace = len(line) - len(line.lstrip())
    if first_nonspace >= 31:
        return ""
    candidate = line[first_nonspace:]
    m = re.match(r"(.*?)(?:\s{2,}|$)", candidate)
    return (m.group(1) if m else candidate).strip()


def qname_from_row(block: str) -> str:
    cells = [first_cell(line) for line in block.splitlines() if first_cell(line)]
    first_area = " ".join(cells)
    compact = re.sub(r"\s+", "", first_area)
    m = re.search(rf"\(((?:{prefixes}):[A-Za-z0-9]+)\)", compact)
    if m:
        return m.group(1)

    # In several source rows pdftotext -layout places second-column Cyrillic
    # text immediately after a wrapped QName fragment. Recover only the
    # explicit ASCII QName fragments printed in the first column; stop once
    # the closing parenthesis is reached. This leaves wildcard XML rows,
    # where no QName is printed at all, unresolved.
    for idx, cell in enumerate(cells):
        start = re.search(rf"\(((?:{prefixes}):([A-Za-z0-9]+))", cell)
        if not start:
            continue
        prefix_and_first = start.group(1)
        first_fragment = start.group(2)
        prefix = prefix_and_first.split(":", 1)[0]
        fragments = [first_fragment]
        if re.search(rf"\({re.escape(prefix_and_first)}\)", cell):
            return prefix_and_first
        for next_cell in cells[idx + 1 : idx + 4]:
            continuation = re.match(r"([A-Za-z0-9]+)\)", next_cell)
            if continuation:
                fragments.append(continuation.group(1))
                return f"{prefix}:{''.join(fragments)}"
            if re.match(r"[A-Za-z0-9]+$", next_cell):
                fragments.append(next_cell)
                continue
            break
    am = re.search(r"атрибут([A-Za-z][A-Za-z0-9]*)", compact, re.I)
    if am:
        return "@" + am.group(1)
    return ""


def field_name_from_row(block: str, label: str, qname: str) -> str:
    parts: list[str] = []
    stopped = False
    for line in block.splitlines():
        seg = first_cell(line)
        if not seg:
            continue
        if not parts:
            seg = re.sub(r"^" + re.escape(label) + r"\s*", "", seg).strip()
        if re.search(rf"\(({prefixes}):", seg):
            before = seg.split("(", 1)[0].strip()
            if before:
                parts.append(before)
            stopped = True
            break
        if re.search(r"\(атрибут\s+[A-Za-z]", seg, re.I):
            before = seg.split("(", 1)[0].strip()
            if before:
                parts.append(before)
            stopped = True
            break
        parts.append(seg)
    name = normalize_space(" ".join(parts))
    if qname.startswith("@"):
        name = re.sub(r"\s*\(атрибут.*$", "", name, flags=re.I).strip()
    if not name:
        name = label.rstrip(".")
    return name[:220]


def multiplicity_from_row(block: str) -> str:
    tokens: list[str] = []
    token_re = re.compile(r"(?:^|\s)(0\.\.\*|1\.\.\*|0\.\.1|1\.\.1|0\.\.|1\.\.|0|1|\*)\s*$")
    for line in block.splitlines():
        if line.startswith("===== PDF_PAGE"):
            continue
        m = token_re.search(line.rstrip())
        if m:
            tokens.append(m.group(1))
    for token in tokens:
        if token in {"0..*", "1..*", "0..1", "1..1"}:
            return token
    for i, token in enumerate(tokens[:-1]):
        if token in {"0..", "1.."} and tokens[i + 1] in {"1", "*"}:
            return token + tokens[i + 1]
    for token in tokens:
        if token in {"0", "1"}:
            return token
    return ""


def description_parts(block: str) -> list[str]:
    parts: list[str] = []
    card_re = re.compile(r"\s+(?:0\.\.\*|1\.\.\*|0\.\.1|1\.\.1|0\.\.|1\.\.|0|1|\*)\s*$")
    for line in block.splitlines():
        if line.startswith("===== PDF_PAGE"):
            continue
        right = line[64:] if len(line) > 64 else ""
        right = card_re.sub("", right).strip()
        if right:
            parts.append(right)
    return parts


def trim_next_row_prelude(parts: list[str]) -> list[str]:
    """Remove right-column type text that visually starts the next table row
    before that next row's first-column label appears in pdftotext -layout output.
    """
    out: list[str] = []
    type_re = re.compile(rf"\b(?:{prefixes}):[A-Za-z0-9]+")
    ruleish_re = re.compile(
        r"Шаблон:|Мин\.|Макс\.|ISO(?:/IEC)?|Нормализованная строка|"
        r"Целое неотрицательное число|Одно из двух значений|Пространство имен|"
        r"Валидация:|Определяется областями|справочник|классификатор|перечн[яе] технических регламентов",
        re.I,
    )
    seen_ruleish = False
    for part in parts:
        if type_re.search(part) and seen_ruleish:
            break
        out.append(part)
        if ruleish_re.search(part):
            seen_ruleish = True
    return out


def pattern_from_parts(parts: list[str]) -> str:
    marker_stops = (
        "Мин. длина:",
        "Макс. длина:",
        "Мин. значение:",
        "Макс. значение:",
        "Нормализованная строка",
        "Определяется областями",
    )
    chunks: list[str] = []
    started = False
    type_re = re.compile(rf"\b(?:{prefixes}):[A-Za-z0-9]+")
    for part in parts:
        if not started:
            if "Шаблон:" not in part:
                continue
            part = part.split("Шаблон:", 1)[1].strip()
            started = True
        elif chunks and (type_re.search(part) or "(M.SDT." in part or "(M.TR.SDT." in part or "(M.CDT." in part or "(M.TR.CDT." in part):
            break
        stop_at = len(part)
        for marker in marker_stops:
            pos = part.find(marker)
            if pos >= 0:
                stop_at = min(stop_at, pos)
        piece = part[:stop_at].strip()
        if piece:
            chunks.append(piece)
        if stop_at < len(part):
            break
    if not chunks:
        return ""
    value = chunks[0]
    for chunk in chunks[1:]:
        unmatched_class = value.count("[") > value.count("]")
        unmatched_quant = value.count("{") > value.count("}")
        if value.endswith("-") or unmatched_class or unmatched_quant:
            value += chunk
        else:
            value += " " + chunk
    return normalize_space(value)


def rules_from_row(parts: list[str], multiplicity: str, field_name: str) -> list[tuple[str, str, str]]:
    desc = normalize_space(" ".join(parts))
    low = desc.lower()
    rules: list[tuple[str, str, str]] = []
    if multiplicity:
        rule_type = "REQUIRED" if multiplicity in {"1", "1..*", "1..1"} else "CONDITIONAL"
        rules.append(("CARDINALITY", rule_type, multiplicity))
    scalar_rules = [
        ("MIN_LENGTH", "LENGTH", r"Мин\. длина:\s*(\d+)"),
        ("MAX_LENGTH", "LENGTH", r"Макс\. длина:\s*(\d+)"),
        ("MAX_DIGITS", "LENGTH", r"Макс\. кол-во цифр:\s*(\d+)"),
        ("MAX_FRACTION_DIGITS", "LENGTH", r"Макс\. кол-во дроб\. цифр:\s*(\d+)"),
        ("MIN_VALUE", "OTHER", r"Мин\. значение:\s*([^.;]+)"),
        ("MAX_VALUE", "OTHER", r"Макс\. значение:\s*([^.;]+)"),
    ]
    for atom, rule_type, regex in scalar_rules:
        for m in re.finditer(regex, desc, re.I):
            rules.append((atom, rule_type, m.group(1).strip()))
    pattern = pattern_from_parts(parts)
    if pattern:
        rules.append(("PATTERN", "PATTERN", pattern))
    if "ISO 8601" in desc:
        rules.append(("ISO_8601", "OTHER", "ISO 8601"))
    if "ISO 639-1" in desc:
        rules.append(("ISO_639_1", "OTHER", "ISO 639-1"))
    if "ISO/IEC" in desc and "9834-8" in desc:
        rules.append(("ISO_IEC_9834_8", "OTHER", "ISO/IEC 9834-8"))
    if "Нормализованная строка" in desc:
        rules.append(("NORMALIZED_STRING", "OTHER", "normalized string"))
    if "Целое неотрицательное число" in desc:
        rules.append(("NONNEGATIVE_INTEGER", "OTHER", "nonnegative integer"))
    if "Одно из двух значений:" in desc and "true" in low and "false" in low:
        rules.append(("BOOLEAN_ENUM", "ENUM", "true|false"))
    if "Пространство имен: любое" in desc:
        rules.append(("ANY_NAMESPACE", "OTHER", "any namespace"))
    if "Валидация: производится всегда" in desc:
        rules.append(("ALWAYS_VALIDATE", "OTHER", "always validate"))
    classifier_terms = (
        "справочником",
        "справочника",
        "классификатором",
        "классификатора",
        "тн вэд еаэс",
        "перечня технических регламентов",
        "перечнем технических регламентов",
        "перечня видов средств (каналов) связи",
        "перечнем видов средств (каналов) связи",
    )
    dependency_scope = f"{field_name} {desc}".lower()
    if any(term in dependency_scope for term in classifier_terms):
        rules.append(("REFERENCE_DATA", "CLASSIFIER", "explicit reference/classifier/list dependency in source row"))
    out: list[tuple[str, str, str]] = []
    seen = set()
    for rule in rules:
        if rule not in seen:
            seen.add(rule)
            out.append(rule)
    return out


def dependency_name(field_name: str, qname: str, desc: str) -> str:
    low = f"{field_name} {qname} {desc}".lower()
    if "communicationchannelcode" in low or "видов средств (каналов) связи" in low:
        return "COMMUNICATION_CHANNEL_KIND_REFERENCE"
    if "processingresult" in low or "результатов обработки" in low:
        return "PROCESSING_RESULTS_REFERENCE"
    if "unifiedcountrycode" in low or "код страны" in low:
        return "COUNTRY_CODE_REFERENCE"
    if "mediatypecode" in low or "форматов данных" in low:
        return "DATA_FORMAT_REFERENCE"
    if qname == "@kindId" or "методов идентификации" in low:
        return "BUSINESS_ENTITY_IDENTIFICATION_METHODS_REFERENCE"
    if "addresskindcode" in low or "видов адресов" in low:
        return "ADDRESS_KIND_REFERENCE"
    if "measure" in low and "unit" in low or "единиц измерения" in low or "единица измерения" in low:
        return "UNIT_OF_MEASUREMENT_REFERENCE"
    if "тн вэд еаэс" in low or "commodity" in low:
        return "TN_VED_EAEU"
    if "conformitydockindcode" in low or "видов документов об оценке соответствия" in low:
        return "CONFORMITY_DOCUMENT_KIND_CLASSIFIER"
    if "docstatuscode" in low and "статус" in low:
        return "CONFORMITY_DOCUMENT_STATUS_CLASSIFIER"
    if "technicalregulationobjectkindcode" in low or "видов объектов технического регулирования" in low:
        return "TECHNICAL_REGULATION_OBJECT_KIND_CLASSIFIER"
    if "technicalregulationid" in low or "технических регламентов" in low:
        return "TECHNICAL_REGULATIONS_LIST"
    if "организационно-правов" in low:
        return "BUSINESS_ENTITY_LEGAL_FORM_REFERENCE"
    if "код стандарта" in low or "standard" in low:
        return "STANDARD_REFERENCE"
    if "dockindcode" in low or "код вида документа" in low:
        return "DOCUMENT_KIND_REFERENCE"
    if qname == "@codeListId" or "идентификатор справочника" in low:
        return "CODELIST_IDENTIFIER_META"
    return "OTHER_EXPLICIT_REFERENCE_DATA"


def external_dependency(field_name: str, qname: str, desc: str) -> str:
    low = f"{field_name} {qname} {desc}".lower()
    if "conformityauthority" in low or "реестру органов по оценке соответствия" in low:
        return "NATIONAL_CONFORMITY_ASSESSMENT_BODY_REGISTER"
    if "technicalregulationid" in low or "перечня технических регламентов" in low:
        return "TECHNICAL_REGULATIONS_LIST"
    if "тн вэд еаэс" in low or "commodity" in low:
        return "TN_VED_EAEU"
    return ""


def engine_capability(atom: str) -> str:
    return {
        "CARDINALITY": "CARDINALITY",
        "MIN_LENGTH": "LENGTH",
        "MAX_LENGTH": "LENGTH",
        "MAX_DIGITS": "NUMERIC_DIGITS",
        "MAX_FRACTION_DIGITS": "NUMERIC_FRACTION_DIGITS",
        "MIN_VALUE": "NUMERIC_RANGE",
        "MAX_VALUE": "NUMERIC_RANGE",
        "PATTERN": "REGEX",
        "ISO_8601": "DATETIME_FORMAT",
        "ISO_639_1": "LANGUAGE_CODE_FORMAT",
        "ISO_IEC_9834_8": "UUID_FORMAT",
        "NORMALIZED_STRING": "NORMALIZED_STRING",
        "NONNEGATIVE_INTEGER": "NONNEGATIVE_INTEGER",
        "BOOLEAN_ENUM": "ENUM",
        "ANY_NAMESPACE": "XML_NAMESPACE",
        "ALWAYS_VALIDATE": "XML_VALIDATION",
        "REFERENCE_DATA": "REFERENCE_DATA_LOOKUP",
    }.get(atom, "GENERIC_VALIDATION")


requirements: list[dict[str, str]] = []
field_rows = Counter()
rule_counter = Counter()
qname_field_rows = Counter()

for structure_id, (start_marker, end_marker, table_no, expected_rows) in structures.items():
    start = text.find(start_marker)
    end = text.find(end_marker, start + 1)
    if start < 0 or end < 0:
        raise RuntimeError(f"Structure block not found: {structure_id}")
    block = text[start:end]
    matches = list(row_pat.finditer(block))
    if len(matches) != expected_rows:
        raise RuntimeError(f"{structure_id}: {len(matches)} field rows, expected {expected_rows}")
    field_rows[structure_id] = len(matches)
    for row_idx, match in enumerate(matches, 1):
        row_block = block[match.start() : matches[row_idx].start() if row_idx < len(matches) else len(block)]
        label = match.group(1)
        qname = qname_from_row(row_block)
        if qname:
            qname_field_rows[structure_id] += 1
        field_name = field_name_from_row(row_block, label, qname)
        multiplicity = multiplicity_from_row(row_block)
        parts = trim_next_row_prelude(description_parts(row_block))
        desc = normalize_space(" ".join(parts))
        source_page = page_at(start + match.start())
        rules = rules_from_row(parts, multiplicity, field_name)
        atom_counts = Counter()
        for atom, rule_type, value in rules:
            atom_counts[atom] += 1
            suffix = f"::{atom}" if atom_counts[atom] == 1 else f"::{atom}.{atom_counts[atom]}"
            canonical_id = f"P.TS.01::{structure_id}::T{table_no:02d}::ROW{row_idx:03d}{suffix}"
            classifier = dependency_name(field_name, qname, desc) if atom == "REFERENCE_DATA" else ""
            ext_dep = external_dependency(field_name, qname, desc)
            if atom == "CARDINALITY":
                normative = f"Кардинальность: {value}"
            elif atom == "PATTERN":
                normative = f"Шаблон: {value}"
            elif atom == "MIN_LENGTH":
                normative = f"Мин. длина: {value}"
            elif atom == "MAX_LENGTH":
                normative = f"Макс. длина: {value}"
            elif atom == "MAX_DIGITS":
                normative = f"Макс. кол-во цифр: {value}"
            elif atom == "MAX_FRACTION_DIGITS":
                normative = f"Макс. кол-во дроб. цифр: {value}"
            elif atom == "REFERENCE_DATA":
                normative = "Явная зависимость от справочника/классификатора/перечня в строке источника"
            else:
                normative = value
            path_tail = qname if qname else "QNAME_NOT_EXPLICITLY_RECOVERED"
            requirements.append(
                {
                    "canonical_id": canonical_id,
                    "PRC": "SHARED_OR_UNRESOLVED_SOURCE_GAP",
                    "TRN": "UNRESOLVED_SOURCE_GAP",
                    "OPR": "UNRESOLVED_SOURCE_GAP",
                    "MSG": structure_messages[structure_id],
                    "source_document": SOURCE_FILE,
                    "PDF page": str(source_page or "UNKNOWN"),
                    "table": f"Таблица {table_no}",
                    "row/item": f"{row_idx}:{label.rstrip('.')}",
                    "normative_text": normative,
                    "structure": structure_id,
                    "field_name_ru": field_name,
                    "field_path": f"{structure_id}/T{table_no}/ROW{row_idx:03d}/{path_tail}",
                    "QName": qname or "PREFIX_QNAME_NOT_RECOVERED_FROM_ROW",
                    "rule_type": rule_type,
                    "classifier_dependency": classifier,
                    "external_registry_dependency": ext_dep,
                    "engine_capability_needed": engine_capability(atom),
                    "source_status": "CONFIRMED_PDF_PREFIX_QNAME" if qname else "CONFIRMED_PDF_QNAME_NOT_RECOVERED",
                    "atom_kind": atom,
                }
            )
            rule_counter[atom] += 1

required_fields = [
    "canonical_id",
    "PRC",
    "TRN",
    "OPR",
    "MSG",
    "source_document",
    "PDF page",
    "table",
    "row/item",
    "normative_text",
    "structure",
    "field_name_ru",
    "field_path",
    "QName",
    "rule_type",
    "classifier_dependency",
    "external_registry_dependency",
    "engine_capability_needed",
    "source_status",
    "atom_kind",
]
with (OUT / "08_REQUIREMENTS.csv").open("w", encoding="utf-8-sig", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=required_fields)
    writer.writeheader()
    writer.writerows(requirements)


classifier_counts = Counter(r["classifier_dependency"] for r in requirements if r["classifier_dependency"])
classifier_pages: dict[str, set[str]] = defaultdict(set)
classifier_where: dict[str, set[str]] = defaultdict(set)
for row in requirements:
    dep = row["classifier_dependency"]
    if dep:
        classifier_pages[dep].add(row["PDF page"])
        classifier_where[dep].add(f"{row['structure']} {row['table']} {row['row/item']}")

classifier_names = {
    "COMMUNICATION_CHANNEL_KIND_REFERENCE": "перечень видов средств (каналов) связи",
    "COUNTRY_CODE_REFERENCE": "справочник (классификатор) кодов стран",
    "DATA_FORMAT_REFERENCE": "справочник форматов данных",
    "PROCESSING_RESULTS_REFERENCE": "справочник результатов обработки электронных документов и сведений",
    "BUSINESS_ENTITY_IDENTIFICATION_METHODS_REFERENCE": "справочник методов идентификации хозяйствующих субъектов",
    "ADDRESS_KIND_REFERENCE": "справочник видов адресов",
    "UNIT_OF_MEASUREMENT_REFERENCE": "справочник единиц измерения",
    "TN_VED_EAEU": "ТН ВЭД ЕАЭС",
    "CONFORMITY_DOCUMENT_KIND_CLASSIFIER": "классификатор видов документов об оценке соответствия",
    "CONFORMITY_DOCUMENT_STATUS_CLASSIFIER": "классификатор статусов действия документа",
    "TECHNICAL_REGULATION_OBJECT_KIND_CLASSIFIER": "классификатор видов объектов технического регулирования",
    "TECHNICAL_REGULATIONS_LIST": "перечень технических регламентов ЕАЭС / Таможенного союза",
    "BUSINESS_ENTITY_LEGAL_FORM_REFERENCE": "справочник организационно-правовых форм",
    "STANDARD_REFERENCE": "справочник стандартов",
    "DOCUMENT_KIND_REFERENCE": "справочник (классификатор) видов документов",
    "CODELIST_IDENTIFIER_META": "идентификатор справочника (классификатора), codeListId",
    "OTHER_EXPLICIT_REFERENCE_DATA": "иная явно указанная справочная зависимость, требующая идентификации",
    "AUTHORITY_ROUTING_DIRECTORY": "справочник идентификаторов органов/организаций для логической адресации",
}

classifier_rows: list[dict[str, str]] = []
for dep in sorted(classifier_counts):
    classifier_rows.append(
        {
            "classifier_id": dep,
            "full_name": classifier_names.get(dep, dep),
            "registry_code": "UNKNOWN",
            "decision_number": "UNKNOWN",
            "decision_date": "UNKNOWN",
            "where_referenced": " | ".join(sorted(classifier_where[dep]))[:1200],
            "requirements_count": str(classifier_counts[dep]),
            "LOCAL_SOURCE_STATUS": "MISSING",
        }
    )
classifier_rows.append(
    {
        "classifier_id": "AUTHORITY_ROUTING_DIRECTORY",
        "full_name": classifier_names["AUTHORITY_ROUTING_DIRECTORY"],
        "registry_code": "UNKNOWN",
        "decision_number": "UNKNOWN",
        "decision_date": "UNKNOWN",
        "where_referenced": "35.1 ОП.pdf, PDF pages 14-15, Regulation clause 12 / section VII reference",
        "requirements_count": "0",
        "LOCAL_SOURCE_STATUS": "EXTERNAL_ONLY",
    }
)
with (OUT / "09_CLASSIFIERS.csv").open("w", encoding="utf-8-sig", newline="") as fh:
    fields = [
        "classifier_id",
        "full_name",
        "registry_code",
        "decision_number",
        "decision_date",
        "where_referenced",
        "requirements_count",
        "LOCAL_SOURCE_STATUS",
    ]
    writer = csv.DictWriter(fh, fieldnames=fields)
    writer.writeheader()
    writer.writerows(classifier_rows)


req_by_structure = Counter(r["structure"] for r in requirements)
domain_model_reqs = req_by_structure["R.TR.TS.01.001"] + req_by_structure["R.TR.TS.01.002"]
generic_version_reqs = req_by_structure["R.004"] + req_by_structure["R.006"] + req_by_structure["R.007"]
external_req_count = sum(1 for r in requirements if r["external_registry_dependency"])

missing_rows: list[dict[str, str]] = []


def add_missing(category, artifact, expected_filename, expected_document_number, where_referenced, pages, requirements_blocked, priority, note):
    missing_rows.append(
        {
            "category": category,
            "artifact": artifact,
            "expected_filename": expected_filename,
            "expected_document_number": expected_document_number,
            "where_referenced": where_referenced,
            "pages": pages,
            "requirements_blocked": str(requirements_blocked),
            "priority": priority,
            "note": note,
        }
    )


add_missing(
    "SOURCE_GAP",
    "Подробная таблица операций/транзакций/сообщений для P.TS.01.PRC.002",
    "UNKNOWN",
    "UNKNOWN",
    "Правила п.11; второй Регламент взаимодействия п.12 обещает таблицу 2, но локальный PDF переходит к следующему документу",
    "8;21-25",
    "UNKNOWN_NOT_ENUMERABLE",
    "P0",
    "Не восстанавливать OPR.004-.008, TRN.003 или MSG.004-.006 по нумерации без источника.",
)

xsd_names = {
    "R.004": "EEC_R_DocDetails_vY.Y.Y.xsd",
    "R.006": "EEC_R_ProcessingResultDetails_vY.Y.Y.xsd",
    "R.007": "EEC_R_ResourceStatusDetails_vY.Y.Y.xsd",
    "R.TR.TS.01.001": "EEC_R_TR_TS_01_ConformityDocsRegistryDetails_v1.0.3.xsd",
    "R.TR.TS.01.002": "EEC_R_TR_TS_01_ConformityDocsRegistryRequestDetails_v1.0.0.xsd",
}
for sid, filename in xsd_names.items():
    add_missing(
        "XSD_MISSING",
        f"XML Schema for {sid}",
        filename,
        "UNKNOWN",
        f"07_STRUCTURES.csv / {sid}",
        "30-94",
        req_by_structure[sid],
        "P0",
        "PDF names the schema but no executable XSD file was found under Документы_xml.",
    )

add_missing("MODEL_PACKAGE_MISSING", "Базовая модель данных vX.X.X", "UNKNOWN", "UNKNOWN", "Импорты всех 5 структур", "30-94", len(requirements), "P0", "Concrete X.X.X version/package is unresolved.")
add_missing("MODEL_PACKAGE_MISSING", "Предметная модель технического регулирования vZ.Z.Z", "UNKNOWN", "UNKNOWN", "Импорты R.TR.TS.01.001/.002", "44-94", domain_model_reqs, "P0", "Concrete Z.Z.Z version/package is unresolved.")
for sid in ("R.004", "R.006", "R.007"):
    add_missing("VERSION_UNRESOLVED", f"Concrete version for {sid} (source uses Y.Y.Y)", xsd_names[sid], "UNKNOWN", f"07_STRUCTURES.csv / {sid}", "29-43", req_by_structure[sid], "P0", "Exact namespace and Clark QName cannot be fixed while Y.Y.Y remains a placeholder.")

for row in classifier_rows:
    add_missing(
        "CLASSIFIER_MISSING" if row["LOCAL_SOURCE_STATUS"] == "MISSING" else "CLASSIFIER_EXTERNAL_ONLY",
        row["full_name"],
        "UNKNOWN",
        row["decision_number"],
        row["where_referenced"],
        ";".join(sorted(classifier_pages.get(row["classifier_id"], set()))) or "14-15",
        row["requirements_count"] or "0",
        "P1" if row["classifier_id"] != "AUTHORITY_ROUTING_DIRECTORY" else "P0",
        "Identifier/version/payload are not established by the scoped PDF; do not invent registry code or decision metadata.",
    )

add_missing("INTEGRATION_HEADER_CONTRACT_MISSING", "Concrete P.TS.01 integration-header/routing contract", "UNKNOWN", "Decision No.5 is referenced; concrete P.TS.01 values UNKNOWN", "01_SOURCE_IDENTITY.md / Decision No.5 boundary", "4;11;14-15;22", "MESSAGE_LEVEL_11", "P0", "Need source-confirmed To/From/ReplyTo/FaultTo/Action/ProcedureID/ConversationID/Integration semantics and routing identifiers required by serialization.")
add_missing("REGISTRY_CONTRACT_MISSING", "Runtime contracts for external registers/reference resources", "UNKNOWN", "UNKNOWN", "10_EXTERNAL_DEPENDENCIES.csv", "5-15;47;62-67;93", external_req_count, "P1", "PDF confirms dependencies but not runtime/API contracts or authoritative snapshots.")
add_missing("NORMATIVE_AMBIGUITY", "Effective date of current Decision No.109 revision", "UNKNOWN", "Decision No.109 dated 23.09.2024", "01_SOURCE_IDENTITY.md", "1-2", 0, "P2", "Current revision identity is confirmed; effective calendar date is not established by this scoped PDF.")

with (OUT / "12_MISSING_MATERIALS.csv").open("w", encoding="utf-8-sig", newline="") as fh:
    fields = ["category", "artifact", "expected_filename", "expected_document_number", "where_referenced", "pages", "requirements_blocked", "priority", "note"]
    writer = csv.DictWriter(fh, fieldnames=fields)
    writer.writeheader()
    writer.writerows(missing_rows)


impl_path = OUT / "13_MESSAGE_IMPLEMENTABILITY.csv"
with impl_path.open("r", encoding="utf-8-sig", newline="") as fh:
    impl_rows = list(csv.DictReader(fh))
for row in impl_rows:
    row["implementability_status"] = "BLOCKED_BY_XSD_MODEL"
with impl_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=list(impl_rows[0].keys()))
    writer.writeheader()
    writer.writerows(impl_rows)


ids = [r["canonical_id"] for r in requirements]
duplicate_ids = len(ids) - len(set(ids))
known_structures = set(structures)
orphan_requirements = sum(1 for r in requirements if r["structure"] not in known_structures)
classifier_inventory = {r["classifier_id"] for r in classifier_rows}
missing_classifier_inventory = sorted({r["classifier_dependency"] for r in requirements if r["classifier_dependency"]} - classifier_inventory)

pattern_rows = [r for r in requirements if r["atom_kind"] == "PATTERN"]
pattern_bleed = [
    r for r in pattern_rows
    if any(marker in r["normative_text"] for marker in ("M.SDT.", "M.TR.SDT.", "ccdo:", "csdo:", "trcdo:", "trsdo:", "M.CDT."))
]

def csv_entities(name: str):
    with (OUT / name).open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


actors = [r for r in csv_entities("02_ACTORS.csv") if r["record_type"] == "ENTITY"]
procedures = [r for r in csv_entities("03_PROCEDURES.csv") if r["record_type"] == "ENTITY"]
operations = [r for r in csv_entities("04_OPERATIONS.csv") if r["record_type"] == "ENTITY"]
transactions = [r for r in csv_entities("05_TRANSACTIONS.csv") if r["record_type"] == "ENTITY"]
messages = [r for r in csv_entities("06_MESSAGES.csv") if r["record_type"] == "ENTITY"]
structure_rows = csv_entities("07_STRUCTURES.csv")
external_deps = csv_entities("10_EXTERNAL_DEPENDENCIES.csv")
source_conflicts = csv_entities("11_SOURCE_CONFLICTS.csv")

prc_codes = {r["procedure_code"] for r in procedures}
opr_codes = {r["operation_code"] for r in operations}
opr_orphans = [r["operation_code"] for r in operations if r["procedure_code"] not in prc_codes]
trn_orphans = []
for r in transactions:
    refs = [x for x in (r["initiator_operation_codes"] + ";" + r["responder_operation_codes"]).split(";") if x]
    if r["procedure_code"] not in prc_codes or any(x not in opr_codes for x in refs):
        trn_orphans.append(r["transaction_code"])
msg_structure_orphans = [r["message_code"] for r in messages if r["structure_id"] not in known_structures]
msg_unresolved_links = [r["message_code"] for r in messages if r["transaction_link_status"] == "UNRESOLVED_SOURCE_GAP"]

requirements_total = len(requirements)
classifier_total = len(classifier_rows)
classifier_present = sum(1 for r in classifier_rows if r["LOCAL_SOURCE_STATUS"] == "PRESENT")
classifier_missing = classifier_total - classifier_present

report = f"""# OP35.1 / P.TS.01 — Initial audit final

STATUS: COMPLETE_WITH_EXPLICIT_SOURCE_GAPS

## Scope

Audit scope is restricted to `/Users/tema/Documents/Work/Документы_xml/35.1 ОП.pdf` and the process `P.TS.01` concerning the unified register of issued conformity certificates and registered declarations of conformity. No facts from other parts of common process No. 35 were used to fill gaps.

## Confirmed inventory

- ACT: {len(actors)}
- PRC: {len(procedures)}
- OPR: {len(operations)} directly source-confirmed; the PRC.002 operation table is absent from the scoped PDF copy and is recorded as a source gap.
- TRN: {len(transactions)} directly source-confirmed; no TRN.003 is inferred.
- MSG: {len(messages)} source-confirmed catalog entries; MSG.004-.006 are not inferred.
- Structures: {len(structure_rows)}
- Structure field rows: {sum(field_rows.values())}
- Atomic requirements: {requirements_total}

## Requirement atomization proof

- Field rows by structure: {dict(field_rows)}
- Requirement atoms by structure: {dict(req_by_structure)}
- Requirement atoms by kind: {dict(rule_counter)}
- CARDINALITY atoms: {rule_counter['CARDINALITY']} (expected 389 from 389 field rows)
- Recovered source prefix QName/attribute token on field rows: {sum(qname_field_rows.values())}/{sum(field_rows.values())}; unresolved rows remain explicit and no Clark QName is synthesized.
- Duplicate canonical IDs: {duplicate_ids}
- Orphan requirements by unknown structure: {orphan_requirements}
- Classifier dependencies absent from `09_CLASSIFIERS.csv`: {len(missing_classifier_inventory)}
- Pattern rows with detected cross-column QName/type bleed: {len(pattern_bleed)}

`field_path` in `08_REQUIREMENTS.csv` is an audit source-row locator (`structure/table/row/QName`), not a synthesized normative XML XPath.

## Source/material blockers

- `P.TS.01.PRC.002`: the PDF confirms the procedure and participants but the promised detailed transaction table is absent before the next approved document begins. Missing OPR/TRN/MSG codes and semantics are not reconstructed.
- XSD files: 0 found locally for the 5 declared structures; all 5 remain missing.
- Generic structures `R.004`, `R.006`, `R.007` use placeholder version `Y.Y.Y`.
- Imported base/domain model versions `X.X.X` / `Z.Z.Z` are unresolved.
- Classifier/reference payload identifiers, registry codes, versions and decision metadata are not established by the scoped PDF unless explicitly stated; unknown values remain `UNKNOWN`.
- Decision No. 5 is referenced, but concrete P.TS.01 integration-header and Action/routing values are not established by this PDF.
- Current revision No.109 dated 23.09.2024 is confirmed; its effective calendar date is not established by this scoped source.

## Integrity

- OPR -> PRC orphan count: {len(opr_orphans)}
- TRN -> PRC/OPR orphan count: {len(trn_orphans)}
- MSG -> unknown structure orphan count: {len(msg_structure_orphans)}
- MSG transaction links explicitly marked `UNRESOLVED_SOURCE_GAP`: {len(msg_unresolved_links)}/{len(messages)}
- SOURCE_CONFLICT records: {len(source_conflicts)}
- External dependencies: {len(external_deps)}

## Implementability

All {len(messages)} source-confirmed messages are `BLOCKED_BY_XSD_MODEL` at this audit boundary. `READY_FOR_IMPLEMENTATION = 0`, `PARTIAL_IMPLEMENTABLE = 0`, `GOLDEN_READY = 0`.

Recommended first message after material closure: `P.TS.01.MSG.002` because it uses the comparatively small `R.007` structure. Before implementation, obtain a concrete `R.007` version/XSD, required imported base-model package(s), the required classifier/reference payloads for its fields, and the source-confirmed P.TS.01 integration-header/routing contract.
"""
(OUT / "15_INITIAL_AUDIT_FINAL.md").write_text(report, encoding="utf-8")


print("FIELD_ROWS", sum(field_rows.values()))
print("QNAME_FIELD_ROWS", sum(qname_field_rows.values()))
print("REQUIREMENTS_TOTAL", requirements_total)
print("BY_STRUCTURE", dict(req_by_structure))
print("BY_RULE", dict(rule_counter))
print("CARDINALITY", rule_counter["CARDINALITY"])
print("CLASSIFIERS_TOTAL", classifier_total)
print("CLASSIFIER_COUNTS", dict(classifier_counts))
print("OTHER_EXPLICIT_REFERENCE_DATA", classifier_counts.get("OTHER_EXPLICIT_REFERENCE_DATA", 0))
print("PATTERN_TOTAL", len(pattern_rows))
print("PATTERN_BLEED", len(pattern_bleed))
print("DUPLICATE_IDS", duplicate_ids)
print("ORPHAN_REQUIREMENTS", orphan_requirements)
print("MISSING_CLASSIFIER_INVENTORY", missing_classifier_inventory)
print("OPR_ORPHANS", opr_orphans)
print("TRN_ORPHANS", trn_orphans)
print("MSG_STRUCTURE_ORPHANS", msg_structure_orphans)
print("MSG_UNRESOLVED_LINKS", len(msg_unresolved_links))
