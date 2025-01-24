def generic_filter(items: list, limit: int=None, **kwargs):
    """
    Filters a list of dictionaries based on multiple key-value pairs.

    Args:
        items (required): List of dictionaries to filter.
        limit: Maximum number of items to return, or None for no limit.
        **kwargs (required): Key-value pairs to filter by (equivalence only).

    Returns:
        list: Filtered and optionally limited list of dictionaries.

    TODO: Offset, different kinds of comparisons, support for other collections
    """
    filtered_items = []
    count = 0

    for item in items:
        if all(item.get(key) == value for key, value in kwargs.items()):
            filtered_items.append(item)
            count += 1
            if limit is not None and count >= limit:
                break # Stop iterating when the limit is reached
    
    return filtered_items
