import math


# 分页配置
def Page(params):
    total_count = int(params['total_count'])
    page_size = int(params['page_size'])
    page = int(params['page'])

    total_pages = math.ceil(total_count / page_size)
    total_pages = total_pages if total_pages > 0 else 1

    is_prev = 0 if page <= 1 else 1
    is_next = 0 if page >= total_pages else 1
    pages = {
        'current': page,
        'total_pages': total_pages,
        'total': total_count,
        'page_size': page_size,
        'is_next': is_next,
        'is_prev': is_prev,
        'range': list(range(1, total_pages + 1)),
        'url': params['url']
    }
    return pages
