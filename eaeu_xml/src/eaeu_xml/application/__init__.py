"""Stable application facade intended for GUI and other interactive clients."""

from eaeu_xml.application.facade import EaeuXmlApplication, TransactionSession
from eaeu_xml.application.models import (
    ConditionEvaluation, ConditionProjection, ConditionResult, ConditionalFieldRule, ConflictGuide, FieldGuide, GuideSearchHit, GuideSourceView, MessageGuide, MessageUsageGuide,
    ProcessGuide, TransactionGuide, FieldView, FormDefinition, FormDisplayMode, FormPresentation, GenerationResult, IssueView, MessageInputSummary, MessageView,
    ProcessIssueView, ProcessView, TransactionView, ValidationView,
)
from eaeu_xml.application.services import ProcessDiscoveryService, TestDataGenerator
from eaeu_xml.application.drafts import DraftDocument, DraftError, DraftLoadResult, DraftService
from eaeu_xml.application.form_filter import FieldVisibilityFilter
from eaeu_xml.application.conditions import ConditionalRuleCompiler, ConditionEvaluator
from eaeu_xml.application.session_snapshot import (
    SESSION_SNAPSHOT_VERSION, SESSION_SUFFIX, SessionMessageSnapshot,
    SessionPersistenceService, SessionSnapshotError, SessionSnapshotValidationResult,
    SessionSnapshotValidator, TransactionSessionSnapshot,
)
from eaeu_xml.application.session_restore import (
    SessionOpenResult, SessionRestoreResult, SessionRestoreStatus, TransactionSessionLifecycleService,
    TransactionSessionRestoreService,
)

__all__ = [
    "EaeuXmlApplication", "TransactionSession", "ProcessDiscoveryService", "TestDataGenerator",
    "ProcessView", "ProcessIssueView", "TransactionView", "MessageView", "FieldView", "FormDefinition", "FormDisplayMode", "FormPresentation", "FieldVisibilityFilter", "MessageInputSummary",
    "IssueView", "ValidationView", "GenerationResult",
    "DraftDocument", "DraftLoadResult", "DraftService", "DraftError",
    "ProcessGuide", "TransactionGuide", "MessageGuide", "MessageUsageGuide", "FieldGuide",
    "GuideSourceView", "GuideSearchHit", "ConflictGuide",
    "ConditionalFieldRule", "ConditionResult", "ConditionEvaluation", "ConditionProjection", "ConditionalRuleCompiler", "ConditionEvaluator",
    "SESSION_SNAPSHOT_VERSION", "SESSION_SUFFIX", "SessionMessageSnapshot",
    "TransactionSessionSnapshot", "SessionSnapshotValidationResult",
    "SessionSnapshotValidator", "SessionPersistenceService", "SessionSnapshotError",
    "SessionRestoreStatus", "SessionRestoreResult", "SessionOpenResult", "TransactionSessionRestoreService",
    "TransactionSessionLifecycleService",
]
