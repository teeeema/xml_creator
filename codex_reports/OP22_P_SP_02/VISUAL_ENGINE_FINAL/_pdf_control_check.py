from pypdf import PdfReader

reader = PdfReader("/Users/tema/Documents/Work/Документы_xml/ОП_22.pdf")
needles = (
    "[0-9a-fA-F]{8}",
    "административно",
    "PostCode",
    "A-Z0-9",
)

for needle in needles:
    pages = []
    for index, page in enumerate(reader.pages):
        if needle in (page.extract_text() or ""):
            pages.append(index + 1)
    print(needle, pages)
