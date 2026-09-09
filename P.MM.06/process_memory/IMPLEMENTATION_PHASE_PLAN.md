# P.MM.06 Implementation Phase Plan

This is an audit plan; no production changes are made.

## Phase 1 — Catalog and transactions

- Scope: Process/ACT/PRC/44 proven OPR/15 TRN/24 MSG
- Prerequisites: completed audits
- Likely files: P.MM.06/process.yaml, actors.yaml, procedures.yaml, operations.yaml, transactions.yaml, messages.yaml, versions.yaml
- Tests: loader/registry, counts, TRN alternatives, TRN.008
- Blockers: B-ACTOR, B-OPR explicit
- Definition of done: loads without invented links/codes

## Phase 2 — Semantic structures

- Scope: 186 nodes, IDs, types, multiplicities
- Prerequisites: phase 1
- Likely files: P.MM.06/structures/*.yaml
- Tests: node counts, hierarchy, cardinality, placeholders
- Blockers: relative *.n links explicit
- Definition of done: all proven semantic nodes represented

## Phase 3 — Semantic MessageRules

- Scope: implement immediate rules and map remaining internal targets
- Prerequisites: phase 2
- Likely files: P.MM.06/message_rules/*.yaml
- Tests: 162 provenance, presence/prohibition/cross-field, external statuses
- Blockers: B-CLASSIFIER, B-EXTERNAL, B-ATTRIBUTE
- Definition of done: all rules retain implementability status

## Phase 4 — Authoritative XML completion

- Scope: QNames, versions, attributes, shared structures, XSD
- Prerequisites: supplementary authoritative sources
- Likely files: structures/*.yaml, versions.yaml, shared/XSD assets
- Tests: QName 186/186, resolver, XSD imports
- Blockers: B-QNAME, B-XSD, B-R006, B-R007, B-VERSION, B-ATTRIBUTE
- Definition of done: no mandatory XML mapping unresolved

## Phase 5 — Serializer/parser/GUI

- Scope: generic serialization, import, complete forms
- Prerequisites: phase 4
- Likely files: eaeu_xml/process_packages/body.py, eaeu_xml/services/xml_serializer.py, eaeu_xml/gui/
- Tests: XML round-trip, 24 body tests, GUI schema
- Blockers: all critical
- Definition of done: all 24 bodies round-trip

## Phase 6 — Classifier and production validation

- Scope: datasets and release gates
- Prerequisites: phases 3–5
- Likely files: classifier assets, P.MM.06/tests/
- Tests: classifier, XSD, full regression
- Blockers: B-CLASSIFIER, B-EXTERNAL
- Definition of done: production gates pass
