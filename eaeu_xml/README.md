# eaeu_xml

`eaeu_xml` is a Python engine and GUI for working with explicitly supplied EAEU XML process packages.

## Requirements

Python 3.11 or newer. The GUI additionally requires wxPython.

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
eaeu-xml-gui /path/to/xml_creator
```

Process packages are direct subdirectories of the supplied root, such as `P.MM.01_OP_26`, `P.MM.06_OP_32`, `P.DS.01_OP_49`, `P.SP.02_OP_22`, and `P.SP.03_OP_23`.
