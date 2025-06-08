from django.db.models import Q

def apply_search_and_sort(queryset, search_value, sort_value, search_fields, sort_mapping):
    if search_value:
        query = Q()
        for field in search_fields:
            query |= Q(**{f"{field}__icontains": search_value})
        queryset = queryset.filter(query)

    sort_field = sort_mapping.get(sort_value)
    if sort_field:
        queryset = queryset.order_by(sort_field)

    return queryset
