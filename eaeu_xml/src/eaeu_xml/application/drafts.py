from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
from typing import Any, Mapping
from xml.etree import ElementTree as ET

from eaeu_xml.application.models import ValidationView


DRAFT_VERSION = 1
DRAFT_SUFFIX = ".eaeudraft.json"


class DraftError(ValueError):
    def __init__(self, code: str, message: str):
        self.code=code; self.message=message; super().__init__(message)


@dataclass(frozen=True)
class DraftDocument:
    draft_version: int
    created_at: str
    updated_at: str
    process_code: str
    process_version: str | None
    transaction_code: str
    message_code: str
    structure_id: str
    structure_version: str | None
    generation_mode: str
    values: Mapping[str, Any]
    session_metadata: Mapping[str, Any] = field(default_factory=dict)
    notes: str | None = None


@dataclass(frozen=True)
class DraftLoadResult:
    document: DraftDocument
    compatible_values: Mapping[str, Any]
    unmapped_values: Mapping[str, Any]
    warnings: tuple[str, ...]
    validation: ValidationView

    @property
    def compatible_count(self): return len(self.compatible_values)
    @property
    def unmapped_count(self): return len(self.unmapped_values)


class DraftService:
    def __init__(self, drafts_root: Path | None = None):
        self.drafts_root=drafts_root or (Path.home()/"EAEU_XML_Drafts")

    @property
    def autosave_path(self): return self.drafts_root/"autosave"/f"autosave_current{DRAFT_SUFFIX}"
    @property
    def clean_shutdown_marker(self): return self.drafts_root/"autosave"/"clean_shutdown.marker"

    def new_document(self, *, process_code, process_version, transaction_code, message_code,
                     structure_id, structure_version, generation_mode, values, session_metadata=None, notes=None,
                     created_at=None):
        now=datetime.now(timezone.utc).isoformat()
        return DraftDocument(DRAFT_VERSION,created_at or now,now,process_code,process_version,transaction_code,message_code,
                             structure_id,structure_version,generation_mode,dict(values),dict(session_metadata or {}),notes)

    def save_draft(self, document: DraftDocument, path: Path) -> Path:
        if document.draft_version!=DRAFT_VERSION:raise DraftError("UNSUPPORTED_DRAFT_VERSION",f"Unsupported draft_version: {document.draft_version}")
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
        payload=asdict(document); payload["values"]=self._encode(document.values); payload["session_metadata"]=self._encode(document.session_metadata)
        text=json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n"
        temporary=None
        try:
            with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=path.parent,prefix=f".{path.name}.",suffix=".tmp",delete=False) as handle:
                temporary=Path(handle.name); handle.write(text); handle.flush(); os.fsync(handle.fileno())
            os.replace(temporary,path)
        finally:
            if temporary and temporary.exists(): temporary.unlink()
        return path

    def load_draft(self, path: Path) -> DraftDocument:
        try:data=json.loads(Path(path).read_text(encoding="utf-8"))
        except (OSError,UnicodeError,json.JSONDecodeError) as error:raise DraftError("DRAFT_INVALID_JSON","Draft is not valid UTF-8 JSON.") from error
        if not isinstance(data,dict):raise DraftError("DRAFT_OBJECT_REQUIRED","Draft root must be an object.")
        if data.get("draft_version")!=DRAFT_VERSION:raise DraftError("UNSUPPORTED_DRAFT_VERSION",f"Unsupported draft_version: {data.get('draft_version')}")
        required=("created_at","updated_at","process_code","transaction_code","message_code","structure_id","generation_mode","values")
        missing=[key for key in required if key not in data]
        if missing:raise DraftError("DRAFT_METADATA_MISSING","Missing draft metadata: "+", ".join(missing))
        if data["generation_mode"] not in {"TEST","STRICT"}:raise DraftError("DRAFT_MODE_INVALID","generation_mode must be TEST or STRICT.")
        if not isinstance(data["values"],dict):raise DraftError("DRAFT_VALUES_INVALID","values must be an object.")
        return DraftDocument(DRAFT_VERSION,str(data["created_at"]),str(data["updated_at"]),str(data["process_code"]),data.get("process_version"),
            str(data["transaction_code"]),str(data["message_code"]),str(data["structure_id"]),data.get("structure_version"),data["generation_mode"],
            self._decode(data["values"]),self._decode(data.get("session_metadata",{})),data.get("notes"))

    def list_recent_drafts(self, limit=10):
        if not self.drafts_root.exists():return ()
        files=[path for path in self.drafts_root.glob(f"*{DRAFT_SUFFIX}") if path.is_file()]
        return tuple(sorted(files,key=lambda path:path.stat().st_mtime,reverse=True)[:limit])

    def autosave(self, document): return self.save_draft(document,self.autosave_path)
    def has_recoverable_autosave(self):
        path=self.autosave_path
        if not path.is_file() or path.stat().st_size==0:return False
        return not self.clean_shutdown_marker.exists() or path.stat().st_mtime>self.clean_shutdown_marker.stat().st_mtime
    def clear_autosave(self):
        if self.autosave_path.exists():self.autosave_path.unlink()
    def mark_clean_shutdown(self):
        self.clean_shutdown_marker.parent.mkdir(parents=True,exist_ok=True); self.clean_shutdown_marker.touch()

    @classmethod
    def _encode(cls,value):
        if isinstance(value,ET.Element):return {"$type":"xml","value":ET.tostring(value,encoding="unicode")}
        if isinstance(value,Mapping):return {str(key):cls._encode(item) for key,item in value.items()}
        if isinstance(value,(list,tuple)):return [cls._encode(item) for item in value]
        if value is None or isinstance(value,(str,int,float,bool)):return value
        raise DraftError("DRAFT_VALUE_NOT_SERIALIZABLE",f"Unsupported draft value type: {type(value).__name__}")

    @classmethod
    def _decode(cls,value):
        if isinstance(value,dict) and value.get("$type")=="xml":
            try:return ET.fromstring(value["value"])
            except (KeyError,ET.ParseError) as error:raise DraftError("DRAFT_XML_VALUE_INVALID","Draft XML fragment is invalid.") from error
        if isinstance(value,dict):return {key:cls._decode(item) for key,item in value.items()}
        if isinstance(value,list):return [cls._decode(item) for item in value]
        return value
