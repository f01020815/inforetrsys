# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
from userworkstation.models import UploadFile


def insert_upload_file(data):
    message = UploadFile()
    num = len(UploadFile.objects)
    new_file_id = num + 1
    message.file_id = new_file_id

    # 存储数据data[inserted_path_id, "./HIGH_LEVEL_EVENT", user_detail[0-2], result['all_files']]
    message.file_path_id = str(data[0])
    message.file_path = data[1]
    message.file_hostname = data[2]
    message.file_ip = data[3]
    message.file_mac = data[4]
    message.file_name = data[5]
    # 保存
    message.save()
    # 提供审批表需要的{id:文档名称}
    approval_n_file_info = {new_file_id:data[5][32:len(data[5])]}
    return approval_n_file_info
