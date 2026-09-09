from dataclasses import dataclass
import re

from eaeu_xml.core.errors import ProcessDefinitionNotFoundError, StructureResolutionError, UnresolvedStructureVersionError
from eaeu_xml.process_packages.body import GenerationMode
from eaeu_xml.process_packages.models import ProcessPackage, StructureDefinition


PLACEHOLDER_PATTERN = re.compile(r"[A-Z](?:\.[A-Z]){2}")


@dataclass(frozen=True)
class StructureResolution:
    definition: StructureDefinition
    active_version: str | None
    uses_version_placeholders: bool
    placeholder_versions: tuple[str, ...] = ()


class StructureVersionResolver:
    def __init__(self, package: ProcessPackage) -> None:
        self.package = package

    def get_active_structure_version(self, structure_id: str) -> StructureDefinition:
        selection=self.package.profile.structures.get(structure_id)
        if selection is None:raise ProcessDefinitionNotFoundError(code="STRUCTURE_PROFILE_NOT_FOUND",message=f"Структура отсутствует в active profile: {structure_id}")
        if selection.active_version is None:raise UnresolvedStructureVersionError(code="UNRESOLVED_STRUCTURE_VERSION",message=f"Active version структуры не разрешена: {structure_id}")
        try:return self.package.structures[(structure_id,selection.active_version)]
        except KeyError as error:raise ProcessDefinitionNotFoundError(code="ACTIVE_STRUCTURE_NOT_FOUND",message=f"Структура {structure_id} версии {selection.active_version} не найдена") from error

    def resolve(self, structure_id: str, *, mode: GenerationMode = GenerationMode.STRICT) -> StructureResolution:
        if isinstance(mode, str): mode=GenerationMode(mode)
        selection = self.package.profile.structures.get(structure_id)
        if selection is None:
            raise ProcessDefinitionNotFoundError(
                code="STRUCTURE_PROFILE_NOT_FOUND",
                message=f"Структура отсутствует в active profile: {structure_id}",
            )
        if selection.active_version is None:
            if mode == GenerationMode.TEST:
                candidates=[definition for (candidate,_),definition in self.package.structures.items() if candidate==structure_id]
                placeholders=[definition for definition in candidates if self.placeholder_versions(definition)]
                if len(placeholders)==1:
                    definition=placeholders[0]
                    return StructureResolution(definition,None,True,self.placeholder_versions(definition))
            raise UnresolvedStructureVersionError(code="UNRESOLVED_STRUCTURE_VERSION",message=f"Active version структуры не разрешена: {structure_id}")
        try:
            definition=self.package.structures[(structure_id, selection.active_version)]
            placeholders=self.placeholder_versions(definition)
            if placeholders and mode==GenerationMode.STRICT:
                raise UnresolvedStructureVersionError(code="UNRESOLVED_STRUCTURE_VERSION",
                    message=f"Структура {structure_id} содержит нормативные placeholders: {', '.join(placeholders)}")
            return StructureResolution(definition,selection.active_version,bool(placeholders),placeholders)
        except KeyError as error:
            raise ProcessDefinitionNotFoundError(
                code="ACTIVE_STRUCTURE_NOT_FOUND",
                message=f"Структура {structure_id} версии {selection.active_version} не найдена",
            ) from error

    @staticmethod
    def placeholder_versions(definition: StructureDefinition) -> tuple[str, ...]:
        texts=(definition.version,definition.namespace or "",*definition.imported_namespaces.values())
        return tuple(dict.fromkeys(match.group(0) for text in texts for match in PLACEHOLDER_PATTERN.finditer(text)))


class StructureResolver:
    """Resolve an explicit structure code/version from registry-loaded catalogs."""

    def resolve(self, *, process: ProcessPackage, structure_code: str,
                version: str) -> StructureDefinition:
        if not version:
            raise StructureResolutionError(
                code="STRUCTURE_VERSION_REQUIRED",
                message="Для разрешения структуры требуется явная версия.",
            )
        try:
            return process.structures[(structure_code, version)]
        except KeyError as error:
            raise ProcessDefinitionNotFoundError(
                code="STRUCTURE_NOT_FOUND",
                message=f"Структура {structure_code} версии {version} не найдена.",
            ) from error
