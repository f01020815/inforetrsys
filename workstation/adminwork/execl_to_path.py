# -*- coding:utf-8 -*-
# Author: Li Gaoyang<gylia@isoftstone.com>
import os
import xlrd
from workstation.publicwork.html_to_path import html_to_path


def execl_to_path(request, files, path, source):
    """
    :param source: 判定是管理员批量插入execl操作还是普通用户操作，指定管理员为'execl'、普通用户为'html'
    :param request: 在此函数中仅用于获取用户的基本信息user_detail使用
    :param files: 该参数由upload_file过滤指定类型文件后生成，仅仅是个list['a.xlsx', 'b.xls']，无法使用file.name方法，请特别注意
    :param path: 对指定目录的文件进行处理
    :return:      CODE可扩展优化   300成功 310域和execl中的列不匹配 320记录重复 330非空域值为空 399未知错误_优化判断逻辑
    """
    count = 0
    for file in files:
        workbook = xlrd.open_workbook(os.path.join(path, file))
        sheet = workbook.sheet_by_index(0)
        rows = sheet.nrows

        for row in range(1, rows):
            # 获取execl每一行的内容
            row_values = sheet.row_values(row)
            data_source = [row_values[0], row_values[1], row_values[2], row_values[3], row_values[4]]
            # 将从execl每个单元格的值按照html_to_path的逻辑处理插入数据库
            inserted_path_id = html_to_path(request, data_source, source)
            if inserted_path_id:
                count += 1
    return count
