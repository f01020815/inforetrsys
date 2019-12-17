# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
import re
from workstation.publicwork.insert_data_arrangement import insert_data_arrangement
from adminworkstation.models import Path
from DBoperation.DBadmin.DBinsertpath import insert_path
from workstation.publicwork.insert_to_SysPath import insert_to_syspath
from workstation.publicwork.insert_to_PartWord import insert_to_partword
from DBoperation.DBuser.DBinsert_pathid import DBinsert_pathid
from workstation.publicwork.log_record import custom, normal

def html_to_path(request, data_source, source):
    """
    :param request: 在此函数中仅用于获取用户的基本信息user_detail使用
    :param data_source: 该参数由upload_file过滤*文件类型后生成，仅仅是个list['a.xlsx', 'b.xls']，无法使用file.name方法，请特别注意
    :param source: 判定是管理员批量插入execl操作还是普通用户操作，指定管理员为'execl'、普通用户为'html'
    :return: 返回插入Path表的path_id
    """
    inserted_path_id = 0
    new_approval_id = 0
    data = insert_data_arrangement(request, data_source, source)
    # 此时列表data[data_source[0-4], user_detai[0-3], display_states, approval_states, hash_value]存放传入数据库的值
    # execl表格插入数据库的判断逻辑：1、 2、 3、 4、 5

    # 1、若输入的交易路径为空，则跳过不处理
    if data[3].isspace() or data[3].strip() == "":
        print("该记录的交易路径项为空，跳过不插入")

    # 2、若输入的交易路径拆分后，长度为0，则跳过不处理
    elif re.split("->|<->|<-|>|》|〉|-〉|\t|——", data[3].strip()) == "":
        print("该记录的交易路径项为空，跳过不插入")

    # 3、若输入的内容已经在Path表中存在，则跳过不处理
    elif len(Path.objects.filter(path_hash=data[10])) != 0:
        print("该记录在Path表中匹配了 %d 笔记录，跳过不插入" % len(Path.objects.filter(path_hash=data[10])))
        custom(request, '重复', data_source, 0)
    # 4、若输入的内容在Path表中匹配不到，则插入数据库Path表
    elif len(Path.objects.filter(path_hash=data[10])) == 0:
        # 插入Path表，并返回插入记录对应的path_id供插入索引表使用
        inserted_path_id = insert_path(request, data)
        # 写入日志
        normal(request, '增加', data_source, inserted_path_id)
        # 插入索引表
        syswords_dict = insert_to_syspath(inserted_path_id)
        insert_to_partword(inserted_path_id, syswords_dict)
        # 普通用户从html插入Path表需要审批，管理员从execl批量插入Path表不需要审批
        if source == 'html':
            # 插入审批表
            new_approval_id = DBinsert_pathid(data, inserted_path_id)
            return inserted_path_id, new_approval_id
        elif source == 'execl':
            pass


    # 5、其他判断逻辑未涉及的原因，异常中断，可优化
    else:
        print("return code:399   ！未知的错误！__请联系管理员优化判断逻辑")

    if source == 'html':
        return inserted_path_id, new_approval_id
    elif source == 'execl':
        return inserted_path_id
