# OP35.1 / P.TS.01 — integration header, Action and routing recovery

## Sources used

- `/Users/tema/Documents/Work/Документы_xml/5 решение.pdf` — Decision of the EEC Collegium No. 5 dated 27.01.2015, generic electronic data exchange rules.
- `/Users/tema/Documents/Work/Документы_xml/35.1 ОП.pdf` — only the P.TS.01 process covered by this audit.

## Generic integration header recovered from Decision No. 5

Decision No. 5 confirms the application-message header contract:

- `wsa:To` — receiver logical address and routing input.
- `wsa:ReplyTo`, `wsa:From`, `wsa:FaultTo` — sender/fault logical-address semantics.
- `wsa:MessageID` — globally unique message identifier; UUID semantics are defined by the rules.
- `wsa:RelatesTo` — links a response/follow-up to the preceding message; technological faults additionally use `int:RelatesAction`.
- `wsa:Action` — URI identifying application-message content.
- `int:ProcedureID` — common-process procedure instance identifier.
- `int:ConversationID` — common-process transaction instance identifier.
- `int:Integration/int:TrackID` and `int:Integration/int:AcceptTime` — values assigned by the integration platform when the message is accepted.

These fields and their generic semantics can be taken from Decision No. 5. Their runtime identifiers are not static P.TS.01 constants.

## P.TS.01-specific Action format

`35.1 ОП.pdf`, PDF page 5, clause 6 confirms:

- process code: `P.TS.01`
- process version: `2.0.0`

Decision No. 5 clauses 59-60 define the component order for an application-message Action. Therefore the source-confirmed generic P.TS.01 form is:

`int://CP/P.TS.01/2.0.0/<PRC>/<TRN>/<MSG>`

ACTION_FORMAT_STATUS: GENERIC_FORMAT_CONFIRMED; EXACT_PER_MESSAGE_ACTIONS_BLOCKED

The remaining blocker is not the URI grammar. The available OP35.1 source does not provide a complete authoritative `TRN -> MSG` linkage for the 11 catalogued messages, and the detailed PRC.002 OPR/TRN/MSG table is absent. Exact Action constants must therefore not be synthesized by matching names or numbering.

## Logical-address format

Decision No. 5 clauses 45-54 confirm:

- fixed prefix `EAEU://`;
- segment `EEC` for the Commission or ISO 3166-1 alpha-2 for a Member State;
- logical-address namespaces `CP`, `CA`, `SR`;
- in `CP`, the participant identifier contains the common-process code, participant code and, when required, an authority/authorized-organization identifier.

For P.TS.01 this yields the source-supported pattern:

`EAEU://<SEGMENT>/CP/P.TS.01/<ACTOR_CODE>[/<AUTHORITY_ID>]`

Examples can be instantiated only where actor and segment are known. The actual national authority identifier must come from the authoritative routing directory; it is not present in the local OP35.1 source set.

## P.TS.01 routing rule and authority directory

`35.1 ОП.pdf`, PDF pages 14-15, Regulation clause 12 states that when one role can be performed by several participants, the logical address additionally contains the identifier of the Member-State authority or authorized organization under Decision No. 5 clause 52. The next paragraph states that this identifier is taken from the directory referenced in section VII of the Rules for information interaction.

Decision No. 5 clauses 52-53 further state that such authority identifiers are used when a role can be performed by multiple participants and are filled according to the lists of Member-State authorities and authorized organizations maintained by the Commission jointly with the authorized bodies.

AUTHORITY_ROUTING_TYPE: A — normative reference directory.

The directory also creates a runtime lookup/configuration dependency, but its primary normative nature is a reference directory, not an API contract or a locally invented configuration table.

Affected scope: application-message routing for roles that can have multiple Member-State participants. This applies to the known P.TS.01 routed transactions/messages involving `P.TS.01.ACT.002`, `.003`, `.004`, and will also apply to the PRC.002 transaction/message set once its missing Table 2 is recovered.

CAN_BE_RESOLVED_BY_DOCUMENT: PARTIAL. A normative document/registry record can identify the directory and version, but practical exact routing also requires the authoritative current directory payload (or equivalent official lookup data) containing the actual authority identifiers.

## Remaining P0 integration/routing sources

1. Complete official PRC.002 regulation content containing the missing Figure 2 / Table 2, so the PRC.002 OPR/TRN/MSG chain is known.
2. Source-confirmed transaction-to-message mappings for exact per-message Action values across the P.TS.01 message catalog where the current consolidated copy is incomplete.
3. Authoritative identifier/version/payload of the authority-routing directory referenced by OP35.1 Regulation clause 12 / section VII of the Rules.

No OP22 Action or routing constants were reused.
