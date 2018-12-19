from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FdfsStorage(Storage):

    def __init__(self):
        self.base_url = settings.FDFS_URL
        self.client_conf = settings.FDFS_CLIENT

    def open(self, name, mode='rb'):
        # 打开文件,文件读取在fastdfs中,不需要本地读取,通过url读取
        pass

    def save(self, name, content, max_length=None):
        # content表示客户端上传的文件对象
        # 保存文件
        # 1. 创建对象
        client = Fdfs_client(settings.FDFS_CLIENT)
        # 2. 上传, 读取请求报文中的文件数据
        result = client.upload_by_buffer(content.read())
        # 3. 返回文件名
        return result['Remote file_id']

    def exists(self, name):
        # 文件不存在本地
        return False

    def url(self, name):
        # 通过nginx访问,返回访问的域名及地址
        print(self.base_url + name)
        return self.base_url + name
