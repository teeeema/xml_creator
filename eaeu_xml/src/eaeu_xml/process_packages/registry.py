"""Index process packages below one explicit root without duplicating loading."""

from pathlib import Path

from eaeu_xml.core.errors import (
    DuplicateProcessCodeError,
    ProcessDefinitionNotFoundError,
    ProcessPackagePathError,
)
from eaeu_xml.process_packages.loader import ProcessPackageLoader
from eaeu_xml.process_packages.models import ProcessPackage
from eaeu_xml.process_packages.versioning import load_process_version
from eaeu_xml.process_packages.readiness import require_package_ready


class ProcessRegistry:
    def __init__(self, processes_root: Path) -> None:
        if not isinstance(processes_root, Path):
            raise ProcessPackagePathError(
                code="EXPLICIT_PATH_REQUIRED",
                message="ProcessRegistry требует явно переданный pathlib.Path.",
            )
        self.root = processes_root.expanduser().resolve()
        if not self.root.is_dir():
            raise ProcessPackagePathError(
                code="PROCESSES_ROOT_NOT_FOUND",
                message=f"Корень process packages не найден: {self.root}",
            )
        shared_root = self.root / "shared" / "structures"
        self.shared_structures = ProcessPackageLoader.load_structures(shared_root)
        self._packages: dict[str, ProcessPackage] = {}
        self._version_packages: dict[tuple[str, str], ProcessPackage] = {}
        self._index()

    def _index(self) -> None:
        for path in sorted(self.root.iterdir(), key=lambda item: item.name):
            if not path.is_dir() or path.name == "shared":
                continue
            if not all((path / name).is_file() for name in ProcessPackageLoader.REQUIRED_FILES):
                continue
            package = ProcessPackageLoader.load(path, shared_structures=self.shared_structures)
            code = package.process.process_code
            if code in self._packages:
                raise DuplicateProcessCodeError(
                    code="DUPLICATE_PROCESS_CODE",
                    message=f"Process code {code} объявлен более чем в одном package.",
                )
            self._packages[code] = package

    def list_processes(self) -> tuple[ProcessPackage, ...]:
        return tuple(self._packages[code] for code in sorted(self._packages))

    def get_process(self, process_code: str, *, version: str | None = None) -> ProcessPackage:
        try:
            package = self._packages[process_code]
        except KeyError as error:
            raise ProcessDefinitionNotFoundError(
                code="PROCESS_NOT_FOUND",
                message=f"Process package не найден: {process_code}",
            ) from error
        if version is None or package.profile.process_version == version:
            require_package_ready(package)
            return package
        if not isinstance(version, str):
            # Let the common selector produce the domain error before cache hashing.
            return load_process_version(package.path, version=version, legacy_package=package)
        key = (process_code, version)
        if key not in self._version_packages:
            self._version_packages[key] = load_process_version(
                package.path,
                version=version,
                shared_structures=self.shared_structures,
                legacy_package=package,
            )
        selected = self._version_packages[key]
        require_package_ready(selected)
        return selected
