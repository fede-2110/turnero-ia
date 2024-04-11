# src/utils/pagination.py
from flask import url_for, request

def paginate(query, page, per_page, endpoint, **kwargs):
    pagination = query.paginate(page, per_page, error_out=False)
    items = pagination.items

    urls = {
        'self': url_for(endpoint, page=page, per_page=per_page, _external=True, **kwargs),
        'next': url_for(endpoint, page=page + 1, per_page=per_page, _external=True, **kwargs) if pagination.has_next else None,
        'prev': url_for(endpoint, page=page - 1, per_page=per_page, _external=True, **kwargs) if pagination.has_prev else None,
        'first': url_for(endpoint, page=1, per_page=per_page, _external=True, **kwargs),
        'last': url_for(endpoint, page=pagination.pages, per_page=per_page, _external=True, **kwargs)
    }

    # Metadatos extendidos
    meta = {
        'page': page,
        'per_page': per_page,
        'total_pages': pagination.pages,
        'total_items': pagination.total,
        'urls': urls
    }

    return items, meta
