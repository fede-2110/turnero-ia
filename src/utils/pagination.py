# src/utils/pagination.py
from flask import url_for, request

def paginate(query, page, per_page,schema, endpoint, **kwargs):
    active_query = query.filter(schema.Meta.model.fecha_baja == None)
    pagination = active_query.paginate(page=page, per_page=per_page, error_out=False)
    items = schema.dump(pagination.items, many=True)

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
