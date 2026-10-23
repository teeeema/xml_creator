from __future__ import annotations
from pathlib import Path
from collections import defaultdict, Counter
from copy import deepcopy
import csv
from collections.abc import Mapping
from eaeu_xml.process_packages.engine import EaeuXmlEngine
from eaeu_xml.process_packages.rules_engine import StructuredRuleEvaluator, RuleStatus

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT / 'P.SP.02_OP_22'
RECON=ROOT / 'codex_reports/OP22_P_SP_02/OP22_IMPLEMENTATION_RECONCILIATION.csv'
ENG=EaeuXmlEngine.load_process(PKG)
IDX=defaultdict(list)
for msg,rs in ENG.rules.items():
    for rule in rs.structured_rules:
        IDX[rule.get('rule_id')].append((msg,rule))
EV=StructuredRuleEvaluator()


def target_field(target):
    return target.get('field') if isinstance(target, Mapping) else target

def abs_field(field, ctx):
    if field == '#text': return ctx
    if ctx and field and field != ctx and not field.startswith(ctx + '/'):
        return f'{ctx}/{field}'
    return field

def set_target(values, target, ctx, value):
    field=target_field(target)
    values[abs_field(field,ctx)] = value

def pick_cmp(op, rhs, truth=True):
    if op == 'EQ': return rhs if truth else ('__DIFF__' if rhs != '__DIFF__' else '__OTHER__')
    if op == 'NE': return ('__DIFF__' if rhs != '__DIFF__' else '__OTHER__') if truth else rhs
    if op == 'IN':
        seq=list(rhs)
        return seq[0] if truth else '__NOT_IN__'
    if op == 'NOT_IN':
        seq=list(rhs)
        return '__NOT_IN__' if truth else seq[0]
    if op in {'GT','GE','LT','LE'}:
        base=float(rhs)
        if op=='GT': return base+1 if truth else base
        if op=='GE': return base if truth else base-1
        if op=='LT': return base-1 if truth else base
        return base if truth else base+1
    raise ValueError(f'unsupported op {op}')

def choose_count(op, rhs, truth):
    rhs=int(rhs)
    candidates=list(range(0,max(rhs+3,4)))
    def ok(n):
        return {'EQ':n==rhs,'NE':n!=rhs,'GT':n>rhs,'GE':n>=rhs,'LT':n<rhs,'LE':n<=rhs}[op]
    for n in candidates:
        if ok(n)==truth: return n
    raise ValueError((op,rhs,truth))

def ensure_selector(values, selector, count=1):
    parent=selector.get('parent') if isinstance(selector,Mapping) else None
    if parent:
        parent_path=ensure_selector(values,parent,1)
    if 'collection' in selector:
        path=selector['collection']
    elif 'qname' in selector:
        path=f"{selector['under']}/{selector['qname']}" if selector.get('under') else selector['qname']
    else:
        raise ValueError(f'bad selector {selector}')
    if count:
        values[path] = 'CTX' if count==1 else ['CTX']*count
    else:
        # avoid any descendant accidentally keeping this selector alive
        for key in list(values):
            if key==path or key.startswith(path+'/'):
                values.pop(key,None)
        return path
    where=selector.get('where')
    if where:
        apply_condition(values,where,path,True)
    return path

def ensure_selector_count(values, selector, count, ctx=None):
    # Current OP22 proof shapes use absolute selectors. When nested under a for_each
    # context, a relative child collection is already encoded as an absolute path.
    return ensure_selector(values,selector,count)

def apply_condition(values, cond, ctx, truth):
    if 'all' in cond:
        items=cond['all']
        if truth:
            for c in items: apply_condition(values,c,ctx,True)
        else:
            if items:
                apply_condition(values,items[0],ctx,False)
                for c in items[1:]: apply_condition(values,c,ctx,True)
        return
    if 'any' in cond:
        items=cond['any']
        if truth:
            if items:
                apply_condition(values,items[0],ctx,True)
                for c in items[1:]:
                    # don't force them false if they touch same field; first true is enough
                    pass
        else:
            for c in items: apply_condition(values,c,ctx,False)
        return
    if 'not' in cond:
        apply_condition(values,cond['not'],ctx,not truth); return
    if 'count' in cond:
        n=choose_count(cond['operator'],cond['value'],truth)
        ensure_selector_count(values,cond['count'],n,ctx)
        return
    field=cond['field']
    rhs=cond.get('value')
    val=pick_cmp(cond['operator'],rhs,truth)
    values[abs_field(field,ctx)] = val

def set_operand(values, operand, ctx, value):
    if isinstance(operand, Mapping):
        if 'selector' in operand:
            p=ensure_selector(values,operand['selector'],1)
            values[abs_field(operand['field'],p)] = value
        else:
            values[abs_field(operand['field'],ctx)] = value
    else:
        values[abs_field(operand,ctx)] = value

def satisfy_comparison(values, assertion, ctx, truth):
    op=assertion['operator']
    if 'right' in assertion:
        rhs='R'
        if op=='EQ': left=rhs if truth else 'L'
        elif op=='NE': left='L' if truth else rhs
        else: raise ValueError('operand comparison non-EQ/NE unsupported')
        set_operand(values,assertion['right'],ctx,rhs)
        set_operand(values,assertion['left'],ctx,left)
    else:
        rhs=assertion.get('right_value')
        left=pick_cmp(op,rhs,truth)
        set_operand(values,assertion['left'],ctx,left)

def apply_assertion(values, a, ctx, truth):
    kind=a['kind']
    if kind=='presence':
        required=a.get('state')=='REQUIRED'
        should_present = required if truth else not required
        field=abs_field(target_field(a['target']),ctx)
        if should_present: values[field]='X'
        else: values.pop(field,None)
        return
    if kind=='fixed_value':
        set_target(values,a['target'],ctx,a.get('value') if truth else '__WRONG__'); return
    if kind=='comparison':
        satisfy_comparison(values,a,ctx,truth); return
    if kind=='conditional_presence':
        apply_condition(values,a['condition'],ctx,True)
        required=a.get('state')=='REQUIRED'
        should_present = required if truth else not required
        field=abs_field(target_field(a['target']),ctx)
        if should_present: values[field]='X'
        else: values.pop(field,None)
        return
    if kind=='conditional_fixed_value':
        apply_condition(values,a['condition'],ctx,True)
        set_target(values,a['target'],ctx,a.get('value') if truth else '__WRONG__'); return
    if kind=='condition':
        apply_condition(values,a['condition'],ctx,truth); return
    if kind=='selection_cardinality':
        mi=a.get('min_occurs',0); ma=a.get('max_occurs')
        if truth:
            n=mi if mi>0 else (1 if ma is None or ma>=1 else 0)
        else:
            n=(ma+1) if ma is not None else (mi-1 if mi>0 else None)
            if n is None: raise ValueError('no negative cardinality')
        ensure_selector_count(values,a['selector'],n,ctx); return
    raise ValueError(kind)

def build_for_each(rule):
    pos={}
    ctx=ensure_selector(pos,rule['selector'],1)
    # parent selector where already ensured by ensure_selector recursion
    for a in rule['assertions']:
        apply_assertion(pos,a,ctx,True)
    # re-apply selector filters in case an assertion touched same field
    if rule['selector'].get('where'): apply_condition(pos,rule['selector']['where'],ctx,True)
    if rule['selector'].get('parent') and rule['selector']['parent'].get('where'):
        p=rule['selector']['parent']['collection']
        apply_condition(pos,rule['selector']['parent']['where'],p,True)
    # Find a targeted negative that actually makes evaluator fail.
    for i,a in enumerate(rule['assertions']):
        neg=deepcopy(pos)
        try: apply_assertion(neg,a,ctx,False)
        except Exception: continue
        # keep selector active after mutation
        if rule['selector'].get('where'): apply_condition(neg,rule['selector']['where'],ctx,True)
        if rule['selector'].get('parent') and rule['selector']['parent'].get('where'):
            p=rule['selector']['parent']['collection']
            apply_condition(neg,rule['selector']['parent']['where'],p,True)
        if EV.evaluate(rule,neg).status is RuleStatus.FAIL:
            return pos,neg,f'assertion[{i}]/{a["kind"]}'
    raise ValueError('no assertion mutation produced FAIL')

def card_counts(rule):
    mi=rule.get('min_occurs',0); ma=rule.get('max_occurs')
    p=mi if mi>0 else (1 if ma is None or ma>=1 else 0)
    n=(ma+1) if ma is not None else (mi-1 if mi>0 else None)
    if n is None: raise ValueError('no invalid cardinality')
    return p,n

def build_cross(rule):
    ls,rs=rule['left']['selector'],rule['right']['selector']
    if ls.get('collection') != rs.get('collection'):
        raise ValueError('different collections unsupported')
    path=ls['collection']
    pos={path:['L','R']}
    # Current OP22 pair uses simple EQ where clauses on same collection.
    lw=ls.get('where'); rw=rs.get('where')
    if not (lw and rw and lw.get('operator')=='EQ' and rw.get('operator')=='EQ' and lw.get('field')==rw.get('field')):
        raise ValueError('cross where shape unsupported')
    wf=abs_field(lw['field'],path)
    pos[wf]=[lw.get('value'),rw.get('value')]
    lf=abs_field(rule['left']['field'],path); rf=abs_field(rule['right']['field'],path)
    pos[lf]=['SAME',None]; pos[rf]=[None,'SAME']
    neg=deepcopy(pos); neg[rf]=[None,'DIFF']
    return pos,neg,'cross_instance_mismatch'

def build_rule(rule):
    kind=rule.get('kind')
    if kind=='for_each': return build_for_each(rule)
    if kind=='selection_cardinality':
        pos={}; neg={}
        if rule.get('when'):
            apply_condition(pos,rule['when'],None,True); apply_condition(neg,rule['when'],None,True)
        p,n=card_counts(rule)
        ensure_selector(pos,rule['selector'],p); ensure_selector(neg,rule['selector'],n)
        return pos,neg,'selection_cardinality'
    if kind=='presence':
        pos={}; neg={}; required=rule.get('state')=='REQUIRED'; field=rule['target']
        if required: pos[field]='X'
        else: neg[field]='X'
        return pos,neg,'presence'
    if kind=='cardinality':
        p,n=card_counts(rule); target=rule['target']
        def vals(k): return {} if k==0 else {target:['X']*k}
        return vals(p),vals(n),'cardinality'
    if kind=='conditional_presence':
        pos={}; neg={}; ctx=ensure_selector(pos,rule['scope'],1); ensure_selector(neg,rule['scope'],1)
        apply_condition(pos,rule['condition'],ctx,True); apply_condition(neg,rule['condition'],ctx,True)
        required=rule.get('state')=='REQUIRED'; pf=abs_field(target_field(rule['target']),ctx)
        if required: pos[pf]='X'
        else: neg[pf]='X'
        return pos,neg,'conditional_presence'
    if kind=='conditional_fixed_value':
        pos={}; neg={}; ctx=ensure_selector(pos,rule['scope'],1); ensure_selector(neg,rule['scope'],1)
        apply_condition(pos,rule['condition'],ctx,True); apply_condition(neg,rule['condition'],ctx,True)
        pf=abs_field(target_field(rule['target']),ctx); pos[pf]=rule.get('value'); neg[pf]='__WRONG__'
        return pos,neg,'conditional_fixed_value'
    if kind=='cross_instance_comparison': return build_cross(rule)
    raise ValueError(f'unsupported top kind {kind}')

def source_covers(row,rule):
    item=row['item']; table=row['source_table']
    def item_covers(spec):
        s=str(spec)
        if s==item: return True
        if '-' in s:
            try:
                a,b=map(int,s.split('-',1)); return a<=int(item)<=b
            except Exception: return False
        return False
    return any(str(ref.get('table'))==table and item_covers(ref.get('item','')) for ref in rule.get('source_refs',[]))



def load_reconciliation_rows():
    return list(csv.DictReader(RECON.open(encoding="utf-8-sig", newline="")))


def component_rule_ids(row):
    return [item.strip() for item in row["current_rule_or_mechanism"].split(",") if item.strip()]


def proof_components(row):
    components = []
    missing = []
    for rule_id in component_rule_ids(row):
        matches = IDX.get(rule_id, [])
        if not matches:
            missing.append(rule_id)
            continue
        covered = [(message, rule) for message, rule in matches if source_covers(row, rule)]
        if not covered:
            missing.append(rule_id)
            continue
        components.extend((rule_id, message, rule) for message, rule in covered)
    return components, missing


def prove_requirement(row):
    components, missing = proof_components(row)
    if missing or not components:
        return False, [], missing or ["NO_SOURCE_COVERED_COMPONENT"]
    results = []
    errors = []
    for rule_id, message, rule in components:
        try:
            positive, negative, mutation = build_rule(rule)
            positive_status = EV.evaluate(rule, positive).status
            negative_status = EV.evaluate(rule, negative).status
        except Exception as exc:
            errors.append(f"{rule_id}: {type(exc).__name__}: {exc}")
            continue
        results.append({
            "rule_id": rule_id,
            "message": message,
            "kind": rule.get("kind", ""),
            "mutation": mutation,
            "positive_status": positive_status.value,
            "negative_status": negative_status.value,
        })
        if positive_status is not RuleStatus.PASS or negative_status is not RuleStatus.FAIL:
            errors.append(
                f"{rule_id}: positive={positive_status.value}, negative={negative_status.value}"
            )
    return not errors, results, errors


def existing_requirement_test_links(row):
    """Return existing OP22 tests that already name this requirement's rule id.

    The linkage is deliberately conservative: the file must name at least one
    complete current rule id and contain both passing and failing validation
    assertions.  The proof-completion test itself is excluded so this function
    only reports evidence that pre-dated this wave.
    """
    test_dir = PKG / "tests"
    rule_ids = component_rule_ids(row)
    links = []
    for path in sorted(test_dir.glob("test_*.py")):
        if path.name == "test_proof_completion.py":
            continue
        text = path.read_text(encoding="utf-8")
        if not any(rule_id in text for rule_id in rule_ids):
            continue
        has_positive = any(
            marker in text
            for marker in (
                "RuleStatus.PASS",
                "_assert_pass",
                "assert result.is_valid",
                "positive",
            )
        )
        has_negative = any(
            marker in text
            for marker in (
                "RuleStatus.FAIL",
                "_assert_fail",
                "assert not result.is_valid",
                "BodyValidationError",
                "pytest.raises",
                "invalid",
            )
        )
        if has_positive and has_negative:
            links.append(path.name)
    return links


def aggregated_atomic_components(row):
    """Resolve an aggregated/inherited row to the atomic rules that prove it.

    A range-only source ref is insufficient on its own.  Each accepted rule
    must also carry a CONFIRMED exact inherited source item for the canonical
    requirement, or an exact current-table source item.
    """
    item = str(row["item"])
    table = str(row["source_table"])
    components = []
    for rule_id in component_rule_ids(row):
        for message, rule in IDX.get(rule_id, []):
            refs = rule.get("source_refs", [])
            exact_current = any(
                str(ref.get("table")) == table and str(ref.get("item")) == item
                for ref in refs
            )
            current_range = any(
                str(ref.get("table")) == table
                and "-" in str(ref.get("item", ""))
                and source_covers(row, rule)
                for ref in refs
            )
            inherited_exact = any(
                str(ref.get("table")) != table
                and str(ref.get("item")) == item
                and ref.get("status") == "CONFIRMED"
                for ref in refs
            )
            if exact_current or (current_range and inherited_exact):
                components.append((rule_id, message, rule))
    return components


def prove_aggregated_requirement(row):
    components = aggregated_atomic_components(row)
    if not components:
        return False, [], ["NO_ATOMIC_SOURCE_LINK"]
    results = []
    errors = []
    for rule_id, message, rule in components:
        try:
            positive, negative, mutation = build_rule(rule)
            positive_status = EV.evaluate(rule, positive).status
            negative_status = EV.evaluate(rule, negative).status
        except Exception as exc:
            errors.append(f"{rule_id}: {type(exc).__name__}: {exc}")
            continue
        results.append({
            "rule_id": rule_id,
            "message": message,
            "kind": rule.get("kind", ""),
            "mutation": mutation,
            "positive_status": positive_status.value,
            "negative_status": negative_status.value,
        })
        if positive_status is not RuleStatus.PASS or negative_status is not RuleStatus.FAIL:
            errors.append(
                f"{rule_id}: positive={positive_status.value}, negative={negative_status.value}"
            )
    return not errors, results, errors
