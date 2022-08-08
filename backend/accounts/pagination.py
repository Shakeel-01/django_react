from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    page_size_query_param = 'records'
    max_page_size = 10000


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_query_param = 'page'
    page_size_query_param = 'records'
    max_page_size = 100

class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'records'
    max_page_size = 15


    


