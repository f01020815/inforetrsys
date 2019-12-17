# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
from adminworkstation.models import SysPath


def insert_syspath(data):
    message = SysPath()
    num = len(SysPath.objects)
    new_syspath_id = num + 1
    message.syspath_id = new_syspath_id

    # 存储数据data[sysname, path_id]
    message.syspath_name = data[0]
    #dictdata = {data[1]:data[2]}
    #str_dictdata = str(dictdata)
    #message.syspath_list = str_dictdata

    # 保存
    message.save()
