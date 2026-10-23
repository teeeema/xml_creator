"""Fail-closed readiness gate for independently stored normative editions."""
import json
import re
from pathlib import Path

from eaeu_xml.process_packages.models import ProcessPackage

from eaeu_xml.core.errors import ProcessPackageValidationError


def is_versioned_package(path: Path) -> bool:
    return path.parent.name == "versions" or (path / "migration_status.json").exists()


def require_package_ready(package: ProcessPackage) -> None:
    """Recheck the passport when a cached package reaches a generation boundary."""
    if is_versioned_package(package.path):
        require_verified_version(
            package.path, version=package.profile.process_version,
            expected_process_code=package.process.process_code,
        )


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
        not isinstance(version, str)
        or re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version) is None
        or metadata.get("target_version") != version
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
