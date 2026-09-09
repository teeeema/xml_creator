"""Machine-readable conditional rules; no text or XML-name interpretation."""

from collections import defaultdict
from dataclasses import replace
from typing import Iterable, Mapping

from eaeu_xml.application.models import (
    ConditionEvaluation, ConditionProjection, ConditionResult,
    ConditionalFieldRule, FieldView, IssueView,
)


OPERATORS = {"EQUALS", "NOT_EQUALS", "IN", "NOT_IN", "PRESENT", "ABSENT", "TRUE", "FALSE"}
EFFECTS = {"SHOW", "HIDE", "REQUIRE", "ENABLE", "DISABLE"}


class ConditionalRuleCompiler:
    """Compiles only an explicit structured `conditional_rule` mapping."""

    def compile(self, business_rules, *, fallback_source_refs=()):
        compiled=[]
        for raw in business_rules:
            item=raw.get("conditional_rule")
            if not isinstance(item,Mapping):continue
            required=("target_field_path","source_field_path","operator","effect")
            if any(not item.get(key) for key in required):continue
            operator=str(item["operator"]).upper();effect=str(item["effect"]).upper()
            if operator not in OPERATORS or effect not in EFFECTS:continue
            refs=tuple(dict.fromkeys(str(ref) for ref in (*fallback_source_refs,*raw.get("source_refs",()),*item.get("source_refs",()))))
            if not refs:continue
            compiled.append(ConditionalFieldRule(
                target_field_path=item["target_field_path"], condition_type=item.get("condition_type",operator),
                source_field_path=item["source_field_path"], operator=operator,
                expected_value=item.get("expected_value"), values=tuple(item.get("values",())), effect=effect,
                source_refs=refs, original_description=raw.get("condition") or item.get("description"),
                rule_id=raw.get("rule_id") or item.get("rule_id"),
            ))
        return tuple(compiled)


class ConditionEvaluator:
    def evaluate(self,rule:ConditionalFieldRule,values:Mapping[str,object]):
        if rule.evaluation_status!="MACHINE_EVALUABLE" or rule.source_field_path not in values:
            return ConditionResult.UNKNOWN
        value=values.get(rule.source_field_path);present=value not in (None,"",(),[],{})
        op=rule.operator
        if op=="PRESENT":return ConditionResult.TRUE if present else ConditionResult.FALSE
        if op=="ABSENT":return ConditionResult.FALSE if present else ConditionResult.TRUE
        if not present:return ConditionResult.UNKNOWN
        if op=="TRUE":answer=value is True
        elif op=="FALSE":answer=value is False
        elif op=="EQUALS":answer=value==rule.expected_value
        elif op=="NOT_EQUALS":answer=value!=rule.expected_value
        elif op=="IN":answer=value in rule.values
        elif op=="NOT_IN":answer=value not in rule.values
        else:return ConditionResult.UNKNOWN
        return ConditionResult.TRUE if answer else ConditionResult.FALSE

    def evaluate_all(self,rules,values):
        return tuple(ConditionEvaluation(rule,self.evaluate(rule,values)) for rule in rules)

    @staticmethod
    def dependency_index(rules):
        index=defaultdict(list)
        for rule in rules:index[rule.source_field_path].append(rule)
        return {path:tuple(items) for path,items in index.items()}

    def project(self,fields:Iterable[FieldView],rules,values,*,diagnostic_paths=(),precomputed_results=None):
        evaluations=(tuple(ConditionEvaluation(rule,precomputed_results[rule]) for rule in rules)
                     if precomputed_results is not None else self.evaluate_all(rules,values));by_target=defaultdict(list)
        for item in evaluations:by_target[item.rule.target_field_path].append(item)
        diagnostic=set(diagnostic_paths);hidden=[]
        def visit_list(items):
            result=[]
            for item in items:
                projected=visit(item)
                if projected is not None:result.append(projected)
            return tuple(result)
        def visit(field):
            current=field;hide=False
            target_evaluations=by_target.get(field.path,())
            if target_evaluations:
                results={item.result.value for item in target_evaluations}
                current=replace(current,conditional_machine_evaluable=True,
                                condition_result=next(iter(results)) if len(results)==1 else "UNKNOWN")
            for evaluation in target_evaluations:
                effect=evaluation.rule.effect;answer=evaluation.result
                if field.path not in diagnostic:
                    if effect=="SHOW" and answer is ConditionResult.FALSE:hide=True
                    elif effect=="HIDE" and answer is ConditionResult.TRUE:hide=True
                if effect=="REQUIRE" and answer is not ConditionResult.UNKNOWN:
                    current=replace(current,required=answer is ConditionResult.TRUE)
                elif effect=="ENABLE" and answer is not ConditionResult.UNKNOWN:
                    current=replace(current,editable=answer is ConditionResult.TRUE)
                elif effect=="DISABLE" and answer is not ConditionResult.UNKNOWN:
                    current=replace(current,editable=answer is ConditionResult.FALSE)
            children=visit_list(current.children);current=replace(current,children=children)
            if hide:
                hidden.extend(item.path for item in self.walk((field,)));return None
            return current
        return ConditionProjection(visit_list(fields),evaluations,tuple(hidden))

    @classmethod
    def walk(cls,fields):
        for field in fields:
            yield field
            yield from cls.walk(field.children)

    def validation_issues(self,rules,values):
        issues=[]
        for evaluation in self.evaluate_all(rules,values):
            rule=evaluation.rule
            if rule.effect=="REQUIRE" and evaluation.result is ConditionResult.TRUE and values.get(rule.target_field_path) in (None,"",(),[],{}):
                issues.append(IssueView("CONDITIONAL_REQUIRED",rule.target_field_path,
                    rule.original_description or "Поле обязательно при выполнении условия.","ERROR",
                    source_ref=", ".join(rule.source_refs) or None,rule_id=rule.rule_id))
        return tuple(issues)

    def evaluate_affected(self,source_field_path,dependency_index,values):
        return {rule:self.evaluate(rule,values) for rule in dependency_index.get(source_field_path,())}
