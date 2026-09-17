.pragma library

function offsetFor(text, line, column) {
    if (line < 1) return -1
    const lines = text.split("\n")
    if (line > lines.length) return -1
    let offset = 0
    for (let index = 0; index < line - 1; index++) offset += lines[index].length + 1
    const safeColumn = column > 0 ? Math.min(column - 1, lines[line - 1].length) : 0
    return offset + safeColumn
}
