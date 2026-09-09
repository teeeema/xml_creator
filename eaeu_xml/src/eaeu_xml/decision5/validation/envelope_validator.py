from eaeu_xml.core.errors import Decision5Error


class EnvelopeValidationError(Decision5Error):
    pass


class EnvelopeValidator:
    def validate(self, message) -> None:
        if message.header is None or message.body_payload is None:
            raise EnvelopeValidationError(code="D5_ENVELOPE_PART", rule_id="D5-XML-ENVELOPE", message="SOAP Envelope требует Header и Body.")
