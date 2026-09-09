# P.MM.01 logical-address audit

## Decision No. 5 rule

Paragraphs 45–47 define `EAEU://` followed by segment, logical-address space
and participant identifier. Paragraph 48/table 6 defines `EEC` for the
Commission segment and ISO 3166-1 alpha-2 for a national segment. Paragraphs
50–53 define a CP participant identifier as process code, process participant
code and an optional authority identifier:

`EAEU://<segment>/CP/<process-code>/<participant-code>[/<authority-id>]`

Paragraph 30 assigns the actual recipient to `wsa:To`. Paragraphs 32 and 34
place the sender address used for a response in `wsa:ReplyTo/wsa:Address`.

## Decision No. 68 participants and TRN.004

Table 1, page 6: Commission = `P.ACT.001`.

Table 1, page 7: competent member-state authority = `P.MM.01.ACT.001`.

Pages 87–90, paragraphs 90–93 and tables 41–42: the member-state authority
executes OPR.020 and sends the request to the Commission; the Commission
executes OPR.021 and returns the information. Pages 187–188/table 10 confirm
MSG.005 as initiating and MSG.006 as response.

Therefore MSG.005 TEST endpoints are:

- To: `EAEU://EEC/CP/P.MM.01/P.ACT.001`
- ReplyTo: `EAEU://RU/CP/P.MM.01/P.MM.01.ACT.001`

MSG.006 reverses these endpoints, receives a new MessageID and relates to the
MSG.005 MessageID. Action remains derived from process 1.1.0, PRC.007,
TRN.004 and the respective MSG code.

## EDocDateTime

Decision No. 68 page 316/table 7 defines `csdo:EDocDateTime` as
`bdt:DateTimeType (M.BDT.00006)` and references ISO 8601. The inspected local
text does not state that a timezone offset is mandatory. Both ISO-formatted
local date-time and offset-bearing date-time remain accepted; no offset-only
validation was introduced.
