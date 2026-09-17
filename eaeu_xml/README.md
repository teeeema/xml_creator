# eaeu_xml

`eaeu_xml` is a Python engine and GUI for working with explicitly supplied EAEU XML process packages.

## Requirements

Python 3.11 or newer. The GUI additionally requires PySide6.

## Install

```sh
cd eaeu_xml
python3 -m pip install -e ".[gui]"
```

## Tests

```sh
cd eaeu_xml
python3 -m pytest -q
```

## GUI

```sh
PYTHONPATH=src python3 -m eaeu_xml.gui_qt /path/to/xml_creator
```

Process packages are direct subdirectories of the supplied root, such as `P.MM.01_OP_26`, `P.MM.06_OP_32`, `P.DS.01_OP_49`, `P.SP.02_OP_22`, and `P.SP.03_OP_23`.
