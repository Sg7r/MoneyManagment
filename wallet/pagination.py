from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    breakpoint()
    page_size = 5  # default number of items per page
    page_size_query_param = 'page_size'  # allows client to specify page size via query parameter
    max_page_size = 100  # maximum items per page


