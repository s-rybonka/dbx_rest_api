

def sort_items_by_name(items, **query_params):
    reverse = False
    ordering = query_params.get('ordering')
    if ordering and 'desc' in ordering:
        reverse = True
    return sorted(
        items, key=lambda k: k['name'].lower(), reverse=reverse
    )

