from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
from typing import Any, Mapping
class RuleStatus(str,Enum): PASS='PASS';FAIL='FAIL';NOT_EVALUATED_EXTERNAL_CONTEXT='NOT_EVALUATED_EXTERNAL_CONTEXT';NOT_EVALUATED_EXTERNAL_REFERENCE='NOT_EVALUATED_EXTERNAL_REFERENCE';UNSUPPORTED_RULE='UNSUPPORTED_RULE'
@dataclass(frozen=True)
class RuleEvaluation: rule_id:str|None;status:RuleStatus;message:str;source_refs:tuple[Mapping[str,Any],...]=()
class StructuredRuleEvaluator:
 def evaluate_all(self,rules,v):return tuple(self.evaluate(r,v) for r in rules)
 def evaluate(self,r,v):
  ext={'EXTERNAL_CONTEXT_REQUIRED':RuleStatus.NOT_EVALUATED_EXTERNAL_CONTEXT,'EXTERNAL_REFERENCE_REQUIRED':RuleStatus.NOT_EVALUATED_EXTERNAL_REFERENCE}
  if r.get('evaluation_status') in ext:return self.out(r,ext[r['evaluation_status']],'External dependency required.')
  k=r.get('kind')
  if k in {'cardinality','presence','fixed_value'}:
   x=v.get(r.get('target'));n=len(x) if isinstance(x,list) else int(x is not None);ok=(r.get('min_occurs',0)<=n and (r.get('max_occurs') is None or n<=r['max_occurs'])) if k=='cardinality' else ((n>0)==(r.get('state')=='REQUIRED') if k=='presence' else x==r.get('value'));return self.out(r,RuleStatus.PASS if ok else RuleStatus.FAIL,'Rule evaluated.')
  if k=='selection_cardinality':
   n=len(self.select(r['selector'],v));ok=r.get('min_occurs',0)<=n and (r.get('max_occurs') is None or n<=r['max_occurs']);return self.out(r,RuleStatus.PASS if ok else RuleStatus.FAIL,'Selection cardinality evaluated.')
  if k=='conditional_presence':
   for x in self.select(r['scope'],v,True):
    if self.c(x.get(r['condition']['field']),r['condition']['operator'],r['condition'].get('value')) and (x.get(r['target']['field']) is not None)==(r['state']=='FORBIDDEN'):return self.out(r,RuleStatus.FAIL,'Conditional presence failed.')
   return self.out(r,RuleStatus.PASS,'Conditional presence evaluated.')
  if k=='aggregate_comparison':
   try:ok=self.c(self.agg(r['left'],v),r['operator'],self.agg(r['right'],v))
   except (InvalidOperation,ValueError,TypeError):ok=False
   return self.out(r,RuleStatus.PASS if ok else RuleStatus.FAIL,'Aggregate comparison evaluated.')
  if k=='comparison':
   try:ok=self.c(v.get(r['left']),r['operator'],v.get(r.get('right'),r.get('right_value')))
   except (KeyError,TypeError,ValueError):ok=False
   return self.out(r,RuleStatus.PASS if ok else RuleStatus.FAIL,'Comparison evaluated.')
  return self.out(r,RuleStatus.UNSUPPORTED_RULE,'Unsupported structured rule.')
 def select(self,s,v,all=False):
  p=s['collection'];n=len(v.get(p,[])) if isinstance(v.get(p),list) else int(v.get(p) is not None);w=s.get('where');return [{k[len(p)+1:]:(z[i] if isinstance(z,list) and i<len(z) else z) for k,z in v.items() if k.startswith(p+'/')} for i in range(n) if all or not w or self.c((v.get(p+'/'+w['field'],[])[i] if isinstance(v.get(p+'/'+w['field']),list) else v.get(p+'/'+w['field'])),w['operator'],w.get('value'))]
 def agg(self,x,v):
  q=[Decimal(str(y[x['value_field']])) for y in self.select(x['selector'],v)];return sum(q,Decimal()) if x['aggregation']=='SUM' else q[0] if len(q)==1 else (_ for _ in ()).throw(ValueError())
 @staticmethod
 def c(a,o,b):
  if o=='EQ':return a==b
  if o=='NE':return a!=b
  if o=='GT':return a>b
  if o=='GE':return a>=b
  if o=='LT':return a<b
  if o=='LE':return a<=b
  raise ValueError(o)
 @staticmethod
 def out(r,s,m):return RuleEvaluation(r.get('rule_id'),s,m,tuple(r.get('source_refs',())))
