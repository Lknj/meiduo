from fdfs_client.client import Fdfs_client

if __name__ == '__main__':
    #1. 根据配置文件, 创建对象
    client = Fdfs_client('client.conf')
    #2. 调用方法, 上传
    result = client.upload_by_filename('/home/python/Desktop/pic/002.jpg')
    print(result)