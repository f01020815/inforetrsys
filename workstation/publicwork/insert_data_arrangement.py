# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
import hashlib
from workstation.publicwork.user_detail import user_detail


def insert_data_arrangement(request, data_source, source):
    """
    :param request: 在此函数中仅用于获取用户的基本信息user_detail使用
    :param data_source: 用户输入数据源（管理员指execl表格的内容，普通用户指在网页上输入的值）
    :param source: 判定是管理员批量插入execl操作还是普通用户操作，指定管理员为'execl'、普通用户为'html'；
                   后续可增加用户类别user_type参数，通过对if判断source和user_type两个值判断
                   实现管理员批量插入execl和通过html插入单条记录（display_approval_states = [1, 1]）
                   普通用户批量插入execl和通过html插入单条记录（display_approval_states = [0, 0]）
    :return: 列表data[data_source[0-4], user_detai[0-3], display_states, approval_states, hash_value]供插入数据库
    """
    data = []
    display_approval_states = []
    data_source_upper = []

    # 对数据源所有字母进行大写转换，并将数据拼接为data_source_upper[]
    for m in range(len(data_source)):
        data_source_upper.extend([data_source[m].upper()])

    # 判断是管理员插入execl，还是普通用户提交数据
    if source == 'html':
        display_approval_states = [1, 0]
    elif source == 'execl':
        display_approval_states = [1, 1]

    # 将用户输入的信息计算md5 hash值
    hash_str = str(data_source_upper[0] + data_source_upper[1] + data_source_upper[2] + data_source_upper[3] + data_source_upper[4])
    object_md5 = hashlib.md5()
    object_md5.update(hash_str.encode(encoding='utf-8'))
    hash_value = [object_md5.hexdigest()]

    data.extend(data_source_upper)
    data.extend(user_detail(request))
    data.extend(display_approval_states)
    data.extend(hash_value)

    # 此时列表data[data_source[0-4], user_detai[0-3], display_states, approval_states, hash_value]存放传入数据库的值

    return data
