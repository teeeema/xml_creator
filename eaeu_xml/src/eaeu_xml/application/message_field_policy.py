from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from eaeu_xml.process_packages.models import MessageFieldPolicyDefinition, MessageFieldPolicyRule, StructureDefinition


@dataclass(frozen=True)
class EffectiveMessageFieldPolicy:
    policy: str
    fixed_value: Any = None
    condition: str | None = None
    external_dependency: str | None = None
    affected_by_req: tuple[str, ...] = ()
    notes: str | None = None
    materialize_when_parent_present: bool = False
    application_enforced: bool = True


class MessageFieldPolicyResolver:
    """Resolve a declarative message-specific policy for every structure field."""

    _CONTEXTUAL_SELECTOR_KEYS = frozenset({"where", "when", "parent", "position", "relative_to_context"})
    _CONTEXTUAL_RULE_KINDS = frozenset({"condition", "conditional_presence", "conditional_fixed_value"})

    @staticmethod
    def _matches(path: str, selector: Mapping[str, str]) -> bool:
        if not selector:
            return False
        if selector.get("path") is not None and path != selector["path"]:
            return False
        prefix = selector.get("path_prefix")
        if prefix is not None and path != prefix and not path.startswith(prefix + "/"):
            return False
        suffix = selector.get("path_suffix")
        if suffix is not None and path != suffix and not path.endswith("/" + suffix):
            return False
        segments = path.split("/")
        qname = selector.get("qname")
        if qname is not None and segments[-1] != qname:
            return False
        ancestor_qname = selector.get("ancestor_qname")
        if ancestor_qname is not None and ancestor_qname not in segments[:-1]:
            return False
        under_path = selector.get("under_path")
        if under_path is not None and not path.startswith(under_path + "/"):
            return False
        return True

    @staticmethod
    def _baseline(structure: StructureDefinition, field) -> EffectiveMessageFieldPolicy:
        by_id = {item.field_id: item for item in structure.presentation_fields}
        ancestors = []
        parent = field.parent
        while parent:
            ancestor = by_id.get(parent)
            if ancestor is None:
                break
            ancestors.append(ancestor)
            parent = ancestor.parent
        structurally_required = (field.min_occurs or 0) > 0
        conditional_ancestor = any((ancestor.min_occurs or 0) == 0 for ancestor in ancestors)
        if structurally_required and conditional_ancestor:
            return EffectiveMessageFieldPolicy(
                "CONDITIONAL",
                condition=f"Обязательно при наличии содержащего реквизита согласно структуре {structure.structure_id}.",
                notes="Структурная обязательность внутри условного родителя.",
            )
        if structurally_required:
            return EffectiveMessageFieldPolicy(
                "REQUIRED", notes=f"Обязательность структуры {structure.structure_id}."
            )
        return EffectiveMessageFieldPolicy(
            "OPTIONAL", notes=f"Допустимый необязательный реквизит структуры {structure.structure_id}."
        )

    @classmethod
    def _is_contextual(cls, value: Mapping[str, Any] | None) -> bool:
        if not isinstance(value, Mapping):
            return False
        return any(key in value for key in cls._CONTEXTUAL_SELECTOR_KEYS)

    @staticmethod
    def _selector_candidates(selector: Mapping[str, Any], paths: tuple[str, ...]) -> tuple[str, ...]:
        collection = selector.get("collection") or selector.get("path")
        if isinstance(collection, str) and collection:
            if collection in paths:
                return (collection,)
            suffix = "/" + collection
            return tuple(path for path in paths if path.endswith(suffix))

        qname = selector.get("qname")
        if not isinstance(qname, str) or not qname:
            return ()
        under = selector.get("under")
        candidates = tuple(path for path in paths if path.split("/")[-1] == qname)
        if not isinstance(under, str) or not under:
            return candidates
        return tuple(
            path for path in candidates
            if path == under or path.startswith(under + "/") or path.endswith("/" + under + "/" + qname)
        )

    @staticmethod
    def _target_candidates(
        base: str,
        target: Mapping[str, Any] | str,
        paths: tuple[str, ...],
    ) -> tuple[str, ...]:
        field = target if isinstance(target, str) else target.get("field") or target.get("path")
        if not isinstance(field, str) or not field:
            return ()

        if base:
            if (field == base or field.startswith(base + "/")) and field in paths:
                return (field,)
            candidate = f"{base}/{field}"
            if candidate in paths:
                return (candidate,)
            return tuple(
                path for path in paths
                if path.startswith(base + "/") and (path == candidate or path.endswith("/" + field))
            )

        if field in paths:
            return (field,)
        suffix = "/" + field
        return tuple(path for path in paths if path == field or path.endswith(suffix))

    @staticmethod
    def _derived_policy(policy: str, rule: Mapping[str, Any], *, fixed_value: Any = None,
                        materialize_when_parent_present: bool = False) -> EffectiveMessageFieldPolicy:
        rule_id = rule.get("rule_id")
        return EffectiveMessageFieldPolicy(
            policy=policy,
            fixed_value=fixed_value,
            affected_by_req=(str(rule_id),) if rule_id else (),
            notes="Безусловная проекция structured rule для формы; runtime-validator остаётся источником проверки.",
            materialize_when_parent_present=materialize_when_parent_present,
            application_enforced=False,
        )

    @staticmethod
    def _merge_derived(
        overlays: dict[str, EffectiveMessageFieldPolicy],
        conflicts: set[str],
        path: str,
        candidate: EffectiveMessageFieldPolicy,
    ) -> None:
        if path in conflicts:
            return
        current = overlays.get(path)
        if current is None:
            overlays[path] = candidate
            return

        reqs = tuple(dict.fromkeys((*current.affected_by_req, *candidate.affected_by_req)))
        if current.policy == candidate.policy:
            if current.policy == "FIXED" and current.fixed_value != candidate.fixed_value:
                overlays.pop(path, None)
                conflicts.add(path)
                return
            overlays[path] = EffectiveMessageFieldPolicy(
                policy=current.policy,
                fixed_value=current.fixed_value,
                affected_by_req=reqs,
                notes=current.notes,
                materialize_when_parent_present=(
                    current.materialize_when_parent_present or candidate.materialize_when_parent_present
                ),
                application_enforced=False,
            )
            return

        if {current.policy, candidate.policy} == {"REQUIRED", "FIXED"}:
            fixed = current if current.policy == "FIXED" else candidate
            overlays[path] = EffectiveMessageFieldPolicy(
                policy="FIXED",
                fixed_value=fixed.fixed_value,
                affected_by_req=reqs,
                notes=fixed.notes,
                materialize_when_parent_present=fixed.materialize_when_parent_present,
                application_enforced=False,
            )
            return

        overlays.pop(path, None)
        conflicts.add(path)

    def resolve_structured_rules(
        self,
        structure: StructureDefinition,
        structured_rules: tuple[Mapping[str, Any], ...],
    ) -> dict[str, EffectiveMessageFieldPolicy]:
        """Project only context-free structured rules into static form policies.

        Contextual selectors and conditional assertions stay exclusively in the
        structured-rule evaluator. Derived policies are visual only and never
        sanitize values or add application-level validation errors.
        """
        paths = tuple(field.path for field in structure.presentation_fields)
        overlays: dict[str, EffectiveMessageFieldPolicy] = {}
        conflicts: set[str] = set()

        def apply(path: str, policy: str, rule: Mapping[str, Any], *, fixed_value: Any = None,
                  materialize_when_parent_present: bool = False) -> None:
            self._merge_derived(
                overlays,
                conflicts,
                path,
                self._derived_policy(
                    policy,
                    rule,
                    fixed_value=fixed_value,
                    materialize_when_parent_present=materialize_when_parent_present,
                ),
            )

        for rule in structured_rules:
            if not isinstance(rule, Mapping):
                continue
            applies_to_structure = rule.get("applies_to_structure")
            if applies_to_structure and applies_to_structure != structure.structure_id:
                continue
            kind = rule.get("kind")
            if kind in self._CONTEXTUAL_RULE_KINDS or any(key in rule for key in ("when", "condition", "scope")):
                continue
            selector = rule.get("selector") if isinstance(rule.get("selector"), Mapping) else {}
            if self._is_contextual(selector):
                continue

            if kind == "selection_cardinality":
                candidates = self._selector_candidates(selector, paths)
                minimum = rule.get("min_occurs") or 0
                maximum = rule.get("max_occurs")
                if maximum == 0 and minimum:
                    continue
                policy = "FORBIDDEN" if maximum == 0 else "REQUIRED" if minimum > 0 else None
                if policy:
                    for path in candidates:
                        apply(path, policy, rule)
                continue

            if kind in {"presence", "fixed_value"}:
                raw_target = rule.get("target")
                target = raw_target if isinstance(raw_target, (str, Mapping)) else {}
                if self._is_contextual(target):
                    continue
                candidates = self._target_candidates("", target, paths)
                if kind == "presence":
                    state = str(rule.get("state") or "").upper()
                    if state not in {"REQUIRED", "FORBIDDEN"}:
                        continue
                    for path in candidates:
                        apply(path, state, rule)
                elif "value" in rule:
                    for path in candidates:
                        apply(path, "FIXED", rule, fixed_value=rule.get("value"))
                continue

            if kind != "for_each":
                continue
            bases = self._selector_candidates(selector, paths)
            assertions = rule.get("assertions")
            if not isinstance(assertions, (list, tuple)):
                continue
            for assertion in assertions:
                if not isinstance(assertion, Mapping):
                    continue
                assertion_kind = assertion.get("kind")
                if assertion_kind in self._CONTEXTUAL_RULE_KINDS or any(
                    key in assertion for key in ("when", "condition", "scope")
                ):
                    continue
                if assertion_kind not in {"presence", "fixed_value"}:
                    continue
                raw_target = assertion.get("target")
                target = raw_target if isinstance(raw_target, (str, Mapping)) else {}
                if self._is_contextual(target):
                    continue
                for base in bases:
                    candidates = self._target_candidates(base, target, paths)
                    if assertion_kind == "presence":
                        state = str(assertion.get("state") or "").upper()
                        if state not in {"REQUIRED", "FORBIDDEN"}:
                            continue
                        for path in candidates:
                            apply(path, state, rule)
                    elif "value" in assertion:
                        for path in candidates:
                            apply(
                                path,
                                "FIXED",
                                rule,
                                fixed_value=assertion.get("value"),
                                materialize_when_parent_present=True,
                            )
        return overlays

    def resolve_all(
        self,
        structure: StructureDefinition,
        definition: MessageFieldPolicyDefinition,
        *,
        structured_rules: tuple[Mapping[str, Any], ...] = (),
    ) -> dict[str, EffectiveMessageFieldPolicy]:
        result: dict[str, EffectiveMessageFieldPolicy] = {}
        derived = self.resolve_structured_rules(structure, structured_rules)
        ordered_rules = sorted(enumerate(definition.rules), key=lambda item: (item[1].priority, item[0]))
        for field in structure.presentation_fields:
            effective = derived.get(field.path, self._baseline(structure, field))
            reqs: list[str] = list(effective.affected_by_req)
            for _, rule in ordered_rules:
                if not self._matches(field.path, rule.selector):
                    continue
                for req in rule.affected_by_req:
                    if req not in reqs:
                        reqs.append(req)
                effective = EffectiveMessageFieldPolicy(
                    policy=rule.policy,
                    fixed_value=rule.fixed_value,
                    condition=rule.condition,
                    external_dependency=rule.external_dependency,
                    affected_by_req=tuple(reqs),
                    notes=rule.notes,
                    materialize_when_parent_present=rule.materialize_when_parent_present,
                    application_enforced=True,
                )
            result[field.path] = effective
        return result

    @staticmethod
    def sanitize_values(values: Mapping[str, object],
                        policies: Mapping[str, EffectiveMessageFieldPolicy]) -> dict[str, object]:
        sanitized = dict(values)
        forbidden = [
            path for path, policy in policies.items()
            if policy.application_enforced and policy.policy == "FORBIDDEN"
        ]
        for path in forbidden:
            for candidate in tuple(sanitized):
                if candidate == path or candidate.startswith(path + "/"):
                    sanitized.pop(candidate, None)

        for path, policy in policies.items():
            if not policy.application_enforced or policy.policy != "FIXED":
                continue
            if policy.materialize_when_parent_present:
                parent = path.rsplit("/", 1)[0] if "/" in path else ""
                parent_present = parent in sanitized or any(
                    candidate != path and candidate.startswith(parent + "/")
                    for candidate in sanitized
                )
                if not parent_present:
                    sanitized.pop(path, None)
                    continue
            sanitized[path] = policy.fixed_value
        return sanitized
