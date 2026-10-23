"""Select immutable legacy packages or explicitly gated versioned catalogs."""
import re
from pathlib import Path

from eaeu_xml.core.errors import (
    ProcessDefinitionNotFoundError,
    ProcessPackageValidationError,
)
from eaeu_xml.process_packages.loader import ProcessPackageLoader
from eaeu_xml.process_packages.models import ProcessPackage
from eaeu_xml.process_packages.readiness import require_package_ready, require_verified_version


_VERSION_PATTERN = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+\Z")


def load_process_version(
    package_path: Path, *, version: str | None = None,
    shared_structures=None,
    legacy_package: ProcessPackage | None = None,
) -> ProcessPackage:
    """Keep the existing package default; never silently fall back for an explicit version."""
    legacy = legacy_package
    if legacy is None:
        legacy = ProcessPackageLoader.load(package_path, shared_structures=shared_structures)
    if version is None or version == legacy.profile.process_version:
        require_package_ready(legacy)
        return legacy

    if not isinstance(version, str) or not _VERSION_PATTERN.fullmatch(version):
        raise ProcessDefinitionNotFoundError(
            code="PROCESS_VERSION_NOT_FOUND",
            message=f"Недопустимый или неизвестный номер версии процесса: {version!r}.",
        )

    versions_root = legacy.path / "versions"
    selected = versions_root / version
    if (
        versions_root.is_symlink()
        or not selected.is_dir()
        or selected.is_symlink()
        or selected.resolve().parent != versions_root.resolve()
    ):
        raise ProcessDefinitionNotFoundError(
            code="PROCESS_VERSION_NOT_FOUND",
            message=f"Версия {version} процесса {legacy.process.process_code} отсутствует.",
        )

    require_verified_version(
        selected, version=version,
        expected_process_code=legacy.process.process_code,
    )

    selected_package = ProcessPackageLoader.load(selected, shared_structures=shared_structures)
    if (
        selected_package.process.process_code != legacy.process.process_code
        or selected_package.profile.process_version != version
    ):
        raise ProcessPackageValidationError(
            code="PROCESS_VERSION_MISMATCH",
            message=f"Нормативный каталог {version} не соответствует запрошенному процессу.",
        )
    return selected_package
