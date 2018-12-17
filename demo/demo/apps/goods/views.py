from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from .models import SKU
from .serializers import SKUSerializer, SKUIndexSerializer
from demo.utils.pagination import StandardResultsSetPagination
from drf_haystack.viewsets import HaystackViewSet


class SKUListView(ListAPIView):
    # queryset = SKU.objects.filter()
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return SKU.objects.filter(category_id=category_id)

    serializer_class = SKUSerializer

    pagination_class = StandardResultsSetPagination

    filter_backends = (OrderingFilter,)
    ordering_fields = ('create_time', 'price', 'sales')


class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]
    serializer_class = SKUIndexSerializer
    pagination_class = StandardResultsSetPagination