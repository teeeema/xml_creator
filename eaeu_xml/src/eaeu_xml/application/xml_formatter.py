"""Safe, standalone XML pretty-printer for the GUI formatter page."""

from xml.dom import minidom


class XmlFormatter:
    @staticmethod
    def _strip_indentation(node):
        children = list(node.childNodes)
        elements = [item for item in children if item.nodeType == item.ELEMENT_NODE]
        meaningful = [item for item in children if item.nodeType == item.TEXT_NODE and item.data.strip()]
        if elements and not meaningful:
            for item in children:
                if item.nodeType == item.TEXT_NODE and not item.data.strip():
                    node.removeChild(item)
        for item in list(node.childNodes):
            if item.nodeType == item.ELEMENT_NODE:
                XmlFormatter._strip_indentation(item)

    def format(self, text: str) -> str:
        document = minidom.parseString(text)
        self._strip_indentation(document)
        return document.toprettyxml(indent="    ")
