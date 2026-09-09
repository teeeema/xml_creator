import json
from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((PACKAGE / name).read_text(encoding="utf-8"))


def records(data, *keys):
    if isinstance(data, list):
        return data
    for key in keys:
        if isinstance(data, dict) and isinstance(data.get(key), list):
            return data[key]
    raise AssertionError(f"Не найден список записей; keys={keys}")


def code_of(row, *keys):
    for key in keys:
        if key in row:
            return row[key]
    raise AssertionError(f"Не найден код в записи: {row}")


def test_process():
    p = load("process.yaml")
    assert p["process_code"] == "P.SP.02"
    assert p["normative_document_number"] == 22
    assert p["active_profile"] == "current"


@pytest.mark.parametrize(
    ("filename", "keys", "code_keys", "prefix", "numbers"),
    [
        ("procedures.yaml", ("procedures",), ("procedure_code", "code"), "P.SP.02.PRC.", range(1, 38)),
        ("operations.yaml", ("operations",), ("operation_code", "code"), "P.SP.02.OPR.", range(1, 201)),
        ("transactions.yaml", ("transactions",), ("transaction_code", "code"), "P.SP.02.TRN.", range(1, 55)),
    ],
)
def test_sequential_catalogs(filename, keys, code_keys, prefix, numbers):
    rows = records(load(filename), *keys)
    actual = [code_of(x, *code_keys) for x in rows]
    expected = [f"{prefix}{n:03d}" for n in numbers]
    assert len(actual) == len(expected)
    assert len(actual) == len(set(actual))
    assert actual == expected


def test_participants():
    rows = records(load("participants.yaml"), "participants")
    codes = [code_of(x, "participant_code", "code") for x in rows]
    assert len(rows) == 4
    assert len(codes) == len(set(codes))


def test_messages():
    rows = records(load("messages.yaml"), "messages")
    codes = [code_of(x, "message_code", "code") for x in rows]
    expected = [
        f"P.SP.02.MSG.{n:03d}"
        for n in range(1, 64)
        if n not in (8, 60)
    ]
    assert len(rows) == 61
    assert len(codes) == len(set(codes))
    assert codes == expected
    assert "P.SP.02.MSG.008" not in codes
    assert "P.SP.02.MSG.060" not in codes


def test_version_profile():
    p = load("version_profiles/current.yaml")
    assert p["process_version"] == "1.0.0"
    assert p["models"]["base"] == "X.X.X"
    assert p["models"]["intellectual_property"] == "Z.Z.Z"

    expected = {
        "R.006": "Y.Y.Y",
        "R.010": "Y.Y.Y",
        "R.IP.SP.02.002": "1.0.0",
        "R.IP.SP.02.007": "1.0.0",
        "R.IP.SP.02.008": "1.0.0",
        "R.IP.SP.03.003": "1.0.0",
    }
    assert set(p["structures"]) == set(expected)
    for sid, version in expected.items():
        assert p["structures"][sid]["active_version"] == version
        assert p["structures"][sid]["source"] == "local"


def test_structure_files_and_counts():
    profile = load("version_profiles/current.yaml")
    expected_rows = {
        "R.006": 10,
        "R.010": 8,
        "R.IP.SP.02.002": 404,
        "R.IP.SP.02.007": 248,
        "R.IP.SP.02.008": 23,
    }
    for sid, meta in profile["structures"].items():
        version = meta["active_version"]
        path = PACKAGE / "structures" / sid / f"{version}.yaml"
        assert path.exists(), f"Нет структуры {path.relative_to(PACKAGE)}"
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["structure_id"] == sid
        assert data["version"] == version
        if sid in expected_rows:
            n = expected_rows[sid]
            assert data["expected_normative_rows"] == n
            assert data["imported_normative_rows"] == n
            assert len(data["fields"]) == n


def test_message_structures_exist_in_profile():
    valid = set(load("version_profiles/current.yaml")["structures"])
    for msg in records(load("messages.yaml"), "messages"):
        ids = []
        if msg.get("structure_id"):
            ids.append(msg["structure_id"])
        ids.extend(msg.get("structure_ids") or [])
        assert ids, f"{msg.get('message_code')} не содержит structure_id/structure_ids"
        assert set(ids) <= valid, f"{msg.get('message_code')}: неизвестные структуры {set(ids)-valid}"


def test_message_rules_catalog():
    rules_dir = PACKAGE / "message_rules"
    expected_nums = (
        [1]
        + list(range(3, 8))
        + list(range(9, 23))
        + [24]
        + list(range(27, 60))
        + list(range(61, 64))
    )
    expected_names = {f"P.SP.02.MSG.{n:03d}.yaml" for n in expected_nums}
    actual_names = {p.name for p in rules_dir.glob("P.SP.02.MSG.*.yaml")}
    assert len(expected_names) == 57
    assert actual_names == expected_names


def test_every_message_rule_file():
    valid_messages = {
        code_of(x, "message_code", "code")
        for x in records(load("messages.yaml"), "messages")
    }
    valid_structures = set(load("version_profiles/current.yaml")["structures"])

    for path in sorted((PACKAGE / "message_rules").glob("P.SP.02.MSG.*.yaml")):
        data = json.loads(path.read_text(encoding="utf-8"))
        msg = data["message_code"]
        assert path.name == f"{msg}.yaml"
        assert msg in valid_messages

        rules = data["business_rules"]
        assert isinstance(rules, list)
        assert rules, f"{path.name}: business_rules пуст"

        rule_ids = []
        for rule in rules:
            rule_ids.append(rule["rule_id"])
            assert rule.get("requirement_code") not in (None, "")
            assert rule.get("applies_to_structure") in valid_structures
            refs = rule.get("source_refs")
            assert isinstance(refs, list) and refs
            for ref in refs:
                assert ref["document"] == "ОП_22.pdf"
                assert ref["version_context"] == "P.SP.02 1.0.0"

        assert len(rule_ids) == len(set(rule_ids)), f"{path.name}: duplicate rule_id"


def test_no_rules_for_messages_without_separate_tables():
    for n in (2, 23, 25, 26, 8, 60):
        assert not (PACKAGE / "message_rules" / f"P.SP.02.MSG.{n:03d}.yaml").exists()


def test_transaction_references_resolve():
    prc = {
        code_of(x, "procedure_code", "code")
        for x in records(load("procedures.yaml"), "procedures")
    }
    opr = {
        code_of(x, "operation_code", "code")
        for x in records(load("operations.yaml"), "operations")
    }
    msg = {
        code_of(x, "message_code", "code")
        for x in records(load("messages.yaml"), "messages")
    }

    rows = records(load("transactions.yaml"), "transactions")

    def walk(value):
        if isinstance(value, dict):
            for v in value.values():
                yield from walk(v)
        elif isinstance(value, list):
            for v in value:
                yield from walk(v)
        elif isinstance(value, str):
            yield value

    for trn in rows:
        code = code_of(trn, "transaction_code", "code")
        strings = list(walk(trn))
        for value in strings:
            if value.startswith("P.SP.02.PRC."):
                assert value in prc, f"{code}: неизвестный PRC {value}"
            elif value.startswith("P.SP.02.OPR."):
                assert value in opr, f"{code}: неизвестный OPR {value}"
            elif value.startswith("P.SP.02.MSG."):
                assert value in msg, f"{code}: неизвестный MSG {value}"
