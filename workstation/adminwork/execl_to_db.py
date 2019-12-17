# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
#
#
#
#
#
#
# ########################################
#
#
#              该函数废弃
#
#
# ########################################
#
#
#
#
#
#
#
#
#
#
#

import os
import xlrd
import hashlib
from adminworkstation.models import Path
from workstation.publicwork.user_detail import user_detail
from DBoperation.DBadmin.DBinsertpath import insert_path


def execl_to_db(request, files, path):
    """
    :param request:
    :param files:
    :param path:
    :return:      CODE可扩展优化   300成功 310域和execl中的列不匹配 320记录重复 330非空域值为空 399未知的_优化判断逻辑
    """

    # 取到Path表所有的内容
    db_hash = []
    fetchall = Path.objects.all()
    for i in fetchall:
        print("i.path_hash")
        db_hash.append(i.path_hash)
        print(db_hash)
    print(db_hash)
    print(type(db_hash))

    # 判断的方法2 ： 获取execl表中每行的hash值和数据库中的path_hash对比是否匹配！！！！！！！！！！！！
    # path_hash = Path.objects.filter(path_hash=1234567890)

    for file in files:
        workbook = xlrd.open_workbook(os.path.join(path, file.name))
        sheet = workbook.sheet_by_index(0)
        rows = sheet.nrows

        # 获取execl每一行的内容
        for row in range(1, rows):
            # 获取execl每行的连接类型/交易描述/交易类型/交易路径/备注
            connection_type = sheet.cell(row, 0).value
            transaction_description = sheet.cell(row, 1).value
            transaction_type = sheet.cell(row, 2).value
            transaction_path = sheet.cell(row, 3).value
            remark = sheet.cell(row, 4).value

            # 获取用户的hostname/IP/MAC
            hostname_ip_mac = user_detail(request)
            # 查询后页面显示状态（1显示，0不显示）管理员上传默认为显示
            display_states = [1]
            # 审批状态（1审批通过，0审批中）管理员上传默认为审批通过
            approval_states = [1]

            # 将execl表的内容和user_detail的信息合并
            execl_path = [connection_type, transaction_description, transaction_type, transaction_path, remark]
            execl_path.extend(hostname_ip_mac)
            # 合并前段页面显示状态和审批状态到execl_path
            execl_path.extend(display_states)
            execl_path.extend(approval_states)
            # 此时列表execl_path[connection_type, transaction_description, transaction_type, transaction_path, remark, \
            # hostname, ip, mac, display_states, approval_states]存放传入数据库的值

            # 对execl中的每一行进行md5 hash放入变量exec_hash   注意：hashlib.md5()的对象只能是str
            # execl中的字符拼接为str
            # execl_hash = execl_path[0]+execl_path[1]+execl_path[2]+execl_path[3]+execl_path[4]
            execl_str = connection_type+transaction_description+transaction_type+transaction_path+remark
            # 创建md5对象
            object_md5 = hashlib.md5()
            # 直接写object_md5.update(str)，报错Unicode-objects must be encoded before hashing
            # python3里默认的str是unicode，需要转换为encoded
            object_md5.update(execl_str.encode(encoding='utf-8'))
            execl_hash = object_md5.hexdigest()
            print(execl_hash)

            # execl插入Path的判断逻辑
            # 若execl每一行的第四列交易路径为空，则跳过不处理
            if sheet.cell(row, 3).value.isspace() or sheet.cell(row, 3).value.strip() == "":
                print(file.name + "的第" + row + "条记录的交易路径项为空，跳过不插入")
                continue
            # 若execl每一行的内容已经在Path表中存在，则跳过不处理
            elif execl_hash in db_hash:
                print(file.name + "的第" + row + "条记录已经在Path表中存在，跳过不插入")
                continue

            # 插入数据库Path表
            else:
                insert_path(execl_path, execl_hash)
                print("插入Path表成功")
    return
