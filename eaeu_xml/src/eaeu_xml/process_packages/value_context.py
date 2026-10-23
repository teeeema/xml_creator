"""Aligned values in a flat path map; list axes belong to their XML parents."""
MISSING = object()


def filled(value):
    if value is MISSING or value is None: return False
    if isinstance(value, str): return bool(value.strip())
    if isinstance(value, list): return any(filled(item) for item in value)
    return True


def field_filled(values, path, context=()):
    return filled(at_context(values, path, context)) or any(
        p.startswith(path + '/') and filled(at_context(values, p, context)) for p in values)


def at_context(values, path, context=()):
    value = values.get(path, MISSING)
    for ancestor, index, count, is_list in context:
        if not path.startswith(ancestor + '/') or not is_list:
            continue
        if isinstance(value, list):
            # Existing flat input may omit a redundant outer axis for a single
            # parent; retain the child's own list rather than truncating it.
            if count == 1 and len(value) != 1:
                continue
            if len(value) != count:
                return MISSING
            value = value[index] if index < len(value) else MISSING
        elif count > 1:
            # A scalar cannot silently fill several repeated parent instances.
            return MISSING
    return value


def present(values, path, context=()):
    raw = at_context(values, path, context)
    if raw is not MISSING and (raw is not None or values.get(path, MISSING) is None or not any(is_list for _, _, _, is_list in context)):
        return True
    return any(p.startswith(path + '/') and at_context(values, p, context) not in (MISSING, None)
               for p in values)


def contexts(values, ancestors):
    current = [()]
    for path in ancestors:
        following = []
        for context in current:
            raw = at_context(values, path, context)
            if raw is MISSING and not present(values, path, context):
                continue
            # None in an aligned parent slot is absence, whereas a scalar None
            # explicitly assigned to a container is the existing group marker.
            if raw is None and not present(values, path, context): continue
            count = len(raw) if isinstance(raw, list) else 1
            for index in range(count):
                following.append((*context, (path, index, count, isinstance(raw, list))))
        current = following
    return current


def leaf_values(value):
    if isinstance(value, list):
        for child in value:
            yield from leaf_values(child)
    elif value is not MISSING:
        yield value
