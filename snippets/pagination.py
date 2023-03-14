from rest_framework.pagination import PageNumberPagination


# custom pagination feature:
# we can simply set pagination in tutorial/settings.py
# but in some case, we will need to custom pagination for each url separately
# such as in snippets list, the page_size = 10, but in snippet category list, the page_size = 15
class CustomPagination(PageNumberPagination):
    page_size = 10
