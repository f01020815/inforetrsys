# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
from adminworkstation.models import PartWord


def insert_pathword(data):
    message = PartWord()
    num = len(PartWord.objects)
    new_partword_id = num + 1
    message.partword_id = new_partword_id

    # 存储数据data[key, path_id]
    message.partword_name = data[0]
    dictdata = {data[1]:data[2]}
    str_dictdata = str(dictdata)
    message.partword_list = str_dictdata

    # 保存
    message.save()
