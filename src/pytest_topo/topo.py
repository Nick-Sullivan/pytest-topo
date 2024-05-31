from typing import Dict

failures = set()
func_name_map = {}


def order_by_dependency(items: Dict):
    for item in items:
        mark = item.get_closest_marker("dependency")
        if not mark:
            continue
        for name in mark.args:
            assert name not in func_name_map, f"Duplicate dependency name found: {name}"
            func_name_map[name] = item.nodeid

    dependencies = {}
    for item in items:
        dependencies[item.nodeid] = []
        mark = item.get_closest_marker("depends_on")
        if not mark:
            continue
        for dep in mark.args:
            func_name = func_name_map[dep]
            dependencies[item.nodeid].append(func_name)

    new_order = list(topological_sort(dependencies))

    new_items = []
    for func_name in new_order:
        new_items.extend([item for item in items if item.nodeid == func_name])

    items[:] = new_items


def topological_sort(source):
    # copy deps so we can modify set in-place
    pending = [(name, set(deps)) for name, deps in source.items()]
    emitted = []
    while pending:
        next_pending = []
        next_emitted = []
        for entry in pending:
            name, deps = entry
            deps.difference_update(emitted)  # remove deps we emitted last pass
            # still has deps? recheck during next pass
            if deps:
                next_pending.append(entry)
            else:
                yield name
                # not required, but helps preserve original ordering
                emitted.append(name)
                # remember what we emitted for difference_update() in next pass
                next_emitted.append(name)

        # all entries have unmet deps, one of two things is wrong...
        if not next_emitted:
            raise ValueError(
                "cyclic or missing dependancy detected: %r" % (next_pending,)
            )
        pending = next_pending
        emitted = next_emitted


def mark_as_failure(item):
    failures.add(item.nodeid)


def should_skip(item):
    mark = item.get_closest_marker("depends_on")
    if not mark:
        return False
    for name in mark.args:
        func_name = func_name_map[name]
        if func_name in failures:
            return True
    return False
