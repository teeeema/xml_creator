"""Immutable historical Body payloads and atomic session bundles."""
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import tempfile
from xml.etree import ElementTree as ET

from eaeu_xml.application.session_snapshot import (
    SessionSnapshotError,
    TransactionSessionSnapshot,
    normalize_session_path,
)

MESSAGE_ARTIFACT_VERSION=1
SESSION_BUNDLE_VERSION=1
SESSION_BUNDLE_SUFFIX=".eaeusession.json"


def _encode(value):
    if isinstance(value,ET.Element):return {"$xml":ET.tostring(value,encoding="unicode")}
    if isinstance(value,list):return {"$list":[_encode(item) for item in value]}
    if isinstance(value,tuple):return {"$tuple":[_encode(item) for item in value]}
    if isinstance(value,dict):return {"$dict":[[str(key),_encode(item)] for key,item in sorted(value.items())]}
    if value is None or isinstance(value,(str,int,float,bool)):return value
    raise SessionSnapshotError("ARTIFACT_PAYLOAD_UNSUPPORTED",f"Unsupported Body value type: {type(value).__name__}")

def _decode(value):
    if isinstance(value,dict) and set(value)=={"$xml"}:return ET.fromstring(value["$xml"])
    if isinstance(value,dict) and set(value)=={"$list"}:return [_decode(item) for item in value["$list"]]
    if isinstance(value,dict) and set(value)=={"$tuple"}:return tuple(_decode(item) for item in value["$tuple"])
    if isinstance(value,dict) and set(value)=={"$dict"}:return {key:_decode(item) for key,item in value["$dict"]}
    if value is None or isinstance(value,(str,int,float,bool)):return value
    raise SessionSnapshotError("ARTIFACT_PAYLOAD_INVALID","Malformed Body payload.")


@dataclass(frozen=True)
class PersistedMessageArtifact:
    message_artifact_version:int
    message_id_ref:str
    transaction_code:str
    message_code:str
    attempt_number:int
    payload_json:str
    payload_sha256:str

    @classmethod
    def from_values(cls,*,message_id_ref,transaction_code,message_code,attempt_number,values):
        payload=json.dumps(_encode(dict(values)),ensure_ascii=False,sort_keys=True,separators=(",",":"))
        return cls(MESSAGE_ARTIFACT_VERSION,message_id_ref,transaction_code,message_code,attempt_number,payload,sha256(payload.encode()).hexdigest())

    def values(self):
        if self.message_artifact_version!=MESSAGE_ARTIFACT_VERSION or sha256(self.payload_json.encode()).hexdigest()!=self.payload_sha256:
            raise SessionSnapshotError("ARTIFACT_INTEGRITY_INVALID","Artifact payload integrity check failed.")
        try:return _decode(json.loads(self.payload_json))
        except Exception as error:raise SessionSnapshotError("ARTIFACT_PAYLOAD_INVALID","Artifact Body payload is invalid.") from error


@dataclass(frozen=True)
class TransactionSessionBundle:
    session_bundle_version:int
    snapshot:TransactionSessionSnapshot
    artifacts:tuple[PersistedMessageArtifact,...]


class SessionBundlePersistenceService:
    def save(self,snapshot,artifacts,path):
        bundle=TransactionSessionBundle(SESSION_BUNDLE_VERSION,snapshot,tuple(artifacts))
        self.validate(bundle)
        text=json.dumps({"session_bundle_version":bundle.session_bundle_version,"snapshot":asdict(snapshot),"artifacts":[asdict(item) for item in bundle.artifacts]},ensure_ascii=False,sort_keys=True,indent=2)+"\n"
        path = normalize_session_path(path)
        path.parent.mkdir(parents=True,exist_ok=True);temporary=None
        try:
            with tempfile.NamedTemporaryFile("w",encoding="utf-8",dir=path.parent,prefix=f".{path.name}.",suffix=".tmp",delete=False) as handle:
                temporary=Path(handle.name);handle.write(text);handle.flush();os.fsync(handle.fileno())
            os.replace(temporary,path)
        finally:
            if temporary and temporary.exists():temporary.unlink()
        return path

    def load(self,path):
        try:data=json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as error:raise SessionSnapshotError("SESSION_BUNDLE_INVALID_JSON","Session bundle is not valid JSON.") from error
        if not isinstance(data,dict) or data.get("session_bundle_version")!=SESSION_BUNDLE_VERSION:
            raise SessionSnapshotError("SESSION_BUNDLE_VERSION_INVALID","Unsupported session bundle version.")
        try:
            from eaeu_xml.application.session_snapshot import SessionMessageSnapshot
            snapshot_data=data["snapshot"];snapshot=TransactionSessionSnapshot(**{**snapshot_data,"history":tuple(SessionMessageSnapshot(**item) for item in snapshot_data["history"])})
            artifacts=tuple(PersistedMessageArtifact(**item) for item in data["artifacts"]);bundle=TransactionSessionBundle(SESSION_BUNDLE_VERSION,snapshot,artifacts)
        except Exception as error:raise SessionSnapshotError("SESSION_BUNDLE_SCHEMA_INVALID","Session bundle schema is invalid.") from error
        self.validate(bundle);return bundle

    @staticmethod
    def validate(bundle):
        if bundle.session_bundle_version!=SESSION_BUNDLE_VERSION:raise SessionSnapshotError("SESSION_BUNDLE_VERSION_INVALID","Unsupported session bundle version.")
        history={item.message_id:item for item in bundle.snapshot.history};seen=set()
        for artifact in bundle.artifacts:
            artifact.values()
            if artifact.message_id_ref in seen:raise SessionSnapshotError("ARTIFACT_DUPLICATE_REFERENCE","Duplicate artifact reference.")
            seen.add(artifact.message_id_ref);record=history.get(artifact.message_id_ref)
            if record is None:raise SessionSnapshotError("ARTIFACT_HISTORY_MISMATCH","Artifact has no session history record.")
            if record.message_code!=artifact.message_code or record.attempt_number!=artifact.attempt_number or bundle.snapshot.transaction_code!=artifact.transaction_code:
                raise SessionSnapshotError("ARTIFACT_MESSAGE_MISMATCH","Artifact does not match its session history record.")
