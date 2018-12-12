from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import AreaInfo
from .serializers import AreaSerializer, SubAreaSerializer
from rest_framework_extensions.cache.mixins import CacheResponseMixin


class AreaViewSet(CacheResponseMixin, ReadOnlyModelViewSet):
    # list ====> 查询列表
    # retrieve =====> 根据主键查询对象
    # queryset = AreaInfo.objects.all()
    def get_queryset(self):
        if self.action == 'list':
            # 查询列表时,返回省的列表
            return AreaInfo.objects.filter(parent__isnull=True)
        else:
            # 查询某个对象时,在此范围内查询
            return AreaInfo.objects.all()

    # serializer_class = AreaSerializer
    def get_serializer_class(self):
        if self.action == "list":
            return AreaSerializer
        else:
            return SubAreaSerializer



