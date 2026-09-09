from dataclasses import dataclass

from eaeu_xml.process_packages.input_policy import ResolvedFieldInputPolicy
from eaeu_xml.process_packages.models import UiInputPolicyDefinition


@dataclass(frozen=True)
class ResolvedUiInputPolicy:
    ui_input_policy: str
    policy_origin: str
    editable: bool
    visible: bool
    reason: str
    reason_code: str | None = None


class UiInputPolicyResolver:
    """Maps normative value-source semantics to presentation behaviour."""

    def resolve(self, *, normative: ResolvedFieldInputPolicy, explicit: UiInputPolicyDefinition | None,
                forbidden: bool, classifier_dataset_available: bool) -> ResolvedUiInputPolicy:
        if forbidden:
            return ResolvedUiInputPolicy("HIDDEN", "DERIVED_FROM_MODEL", False, False,
                                         "MessageRules marks the field forbidden/not used.", "OTHER")
        if explicit:
            return self._result(explicit.ui_input_policy, explicit.policy_origin, explicit.reason)
        policy = normative.input_policy
        if policy in {"AUTO_FIXED", "AUTO_GENERATED", "AUTO_DATETIME", "CORRELATION"}:
            return ResolvedUiInputPolicy("READ_ONLY", "DERIVED_FROM_MODEL", False, True,
                                         f"Normative value source is {policy}; the value is shown but not edited.")
        if policy == "INTEGRATION_PLATFORM":
            return ResolvedUiInputPolicy("HIDDEN", "DERIVED_FROM_MODEL", False, False,
                                         "The integration platform supplies this technical value.")
        if policy == "CLASSIFIER":
            if classifier_dataset_available:
                return ResolvedUiInputPolicy("USER_SELECT", "DERIVED_FROM_MODEL", True, True,
                                             "The application has a classifier dataset for selection.")
            return ResolvedUiInputPolicy("USER_INPUT", "DERIVED_FROM_MODEL", True, True,
                                         "TEST fallback is used because the classifier dataset is unavailable.")
        if policy == "STRUCTURAL_CONTAINER":
            return ResolvedUiInputPolicy("GROUP", "DERIVED_FROM_MODEL", False, True,
                                         "Complex container is presented as a visual group.")
        if policy == "EXTERNAL_SYSTEM":
            return ResolvedUiInputPolicy("EXTERNAL_SYSTEM", "DERIVED_FROM_MODEL", False, True,
                                         "The value must arrive from an external information system.")
        if policy == "CONDITIONAL":
            return ResolvedUiInputPolicy("UNRESOLVED_UI_POLICY", "DERIVED_FROM_MODEL", False, True,
                                         "The condition is known, but the provider after activation is not.",
                                         "CONDITIONAL_SOURCE_UNKNOWN")
        if policy == "USER_SELECT":
            return ResolvedUiInputPolicy("USER_SELECT", "NORMATIVE", True, True, "Closed values are confirmed by the model.")
        if policy == "USER_INPUT":
            return ResolvedUiInputPolicy("USER_INPUT", "NORMATIVE", True, True, "Manual input is confirmed by policy metadata.")
        if policy == "UNRESOLVED_INPUT_POLICY":
            return ResolvedUiInputPolicy("USER_INPUT", "PROJECT_UI_DEFAULT", True, True,
                                         "Project UX fallback: no automatic, classifier, external, conditional or structural source applies.")
        return ResolvedUiInputPolicy("UNRESOLVED_UI_POLICY", "DERIVED_FROM_MODEL", False, True,
                                     f"No UI mapping is defined for normative policy {policy}.", "INSUFFICIENT_METADATA")

    @staticmethod
    def _result(policy: str, origin: str, reason: str) -> ResolvedUiInputPolicy:
        return ResolvedUiInputPolicy(policy, origin, policy in {"USER_INPUT", "USER_SELECT"}, policy != "HIDDEN", reason)
