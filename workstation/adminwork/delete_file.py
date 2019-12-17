# -*- coding:utf-8 -*-
# Author: Li Gaoyang<gylia@isoftstone.com>
import glob
import os


def delete_file(path, file_types):
    """
    删除指定目录指定类型文件
    :param path: 指定的目录
    :param file_types: 指定的文件类型（使用扩展名区分不同类型的文件，扩展名不区分大小写，可使用['*']代表所有文件）
    :return: None
    """
    for file_type in file_types:
        files = glob.glob(os.path.join(path, r'*.') + file_type)
        for file in files:
            os.remove(file)
    return
