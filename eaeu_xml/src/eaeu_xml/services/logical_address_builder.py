from eaeu_xml.decision5.models.address import LogicalAddress


class LogicalAddressBuilder:
    """Build a CP address from caller-supplied normative components."""

    def build_common_process(
        self,
        *,
        segment: str,
        process_code: str,
        participant_code: str,
        authority_identifier: str | None = None,
    ) -> LogicalAddress:
        components = ["EAEU:", "", segment, "CP", process_code, participant_code]
        if authority_identifier:
            components.append(authority_identifier)
        return LogicalAddress.parse("/".join(components))
