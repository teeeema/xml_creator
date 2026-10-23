"""Fail-closed readiness gate for independently stored normative editions."""
import json
from pathlib import Path

from eaeu_xml.core.errors import ProcessPackageValidationError


def require_verified_version(
    path: Path, *, version: str, expected_process_code: str | None = None,
) -> None:
    status_path = path / "migration_status.json"
    try:
        metadata = json.loads(status_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ProcessPackageValidationError(
            code="PROCESS_VERSION_NOT_READY",
            message=f"Версия {version}: отсутствует или повреждён паспорт готовности.",
        ) from error

    if not isinstance(metadata, dict) or (
        metadata.get("target_version") != version
        or (
            expected_process_code is not None
            and metadata.get("process_code") != expected_process_code
        )
        or metadata.get("state") != "VERIFIED_READY"
        or metadata.get("promotion_allowed") is not True
    ):
        raise ProcessPackageValidationError(
            code="PROCESS_VERSION_NOT_READY",
            message=f"Нормативная версия {version} ещё не прошла приёмку.",
        )
