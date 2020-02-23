from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client

# 自定义的文件存储类 (继承Storage)
# 后台Admin管理站点中，就是通过Storage类来实现文件的上传/下载。
class FDFSStorage(Storage):
    '''fastDFS 文件存储类'''
    def __init__(self, client_conf=None, base_url=None):
        '''初始化'''
        if client_conf is None:
            client_conf = settings.FDFS_CLIENT_CONF
        self.client_conf = client_conf

        if base_url is None:
            base_url = settings.FDFS_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        '''打开文件时使用'''
        pass

    def _save(self, name, content):
        '''保存文件时使用'''
        # name： 你选择上传文件的名字
        # content： 包含你上传文件内容的File对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_conf)

        # print(type(name))
        # print(type(content))

        # 上传文件到fastDFS系统中
        # upload_by_buffer可以直接对File对象的内容读取进行上传，upload_by_filename只能根据文件的名字上传内容
        res = client.upload_by_buffer(content.read())

        # print(res)
        # res的内容为字典，包括以下内容
        # dict
        # {
        #     'Group name': group_name,
        #     'Remote file_id': remote_file_id,
        #     'Status': 'Upload successed.',   上传成功
        #     'Local file name': '',
        #     'Uploaded size': upload_size,
        #     'Storage IP': storage_ip
        # }

        if res.get('Status') != 'Upload successed.':
            # 上传失败
            print('上传文件到fastDFS失败')
            raise Exception('上传文件到fastDFS失败')


        # 获取返回的文件ID
        filename = res.get('Remote file_id')

        return filename  # 返回的内容,就会保存到Django的数据库中(后台Admin管理站点)。

    def exists(self, name):
        '''Django判断文件名是否可用'''
        return False

    # 前端模板页中，img标签的src会用到该方法返回值
    def url(self, name):
        '''返回访问文件的url路径'''
        return self.base_url+name