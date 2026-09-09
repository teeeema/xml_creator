from eaeu_xml.decision5.models.address import LogicalAddress


class LogicalAddressValidator:
    def validate(self, address: LogicalAddress) -> None:
        LogicalAddress.parse(address.serialize())
