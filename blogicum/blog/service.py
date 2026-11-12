from django.core.paginator import Paginator

from .constants import POSTS_BY_PAGE


def paginate_queryset(request, queryset, per_page=POSTS_BY_PAGE):
    """Разбить queryset на страницы и вернуть Page из GET-параметра."""
    return Paginator(queryset, per_page).get_page(
        request.GET.get('page')
    )
