from django.core.paginator import Paginator

from .constants import POSTS_BY_PAGE


def paginate_queryset(request, queryset):
    """Разбить queryset на страницы и вернуть Page из GET-параметра."""
    return Paginator(queryset, POSTS_BY_PAGE).get_page(
        request.GET.get('page')
    )
