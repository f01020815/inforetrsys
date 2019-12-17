# -*- coding:utf-8 -*-
# Author: Li Gaoyang<gylia@isoftstone.com>
import os
from django.utils import timezone   # 获取当前时间
import hashlib   # 给当前时间编码


def upload_file(files, path, file_types):
    """
    :param files: 前端用户上传的一个或多个文件list
    :param path: 文件上传到指定目录
                 目前只有三个目录BASE_DIR/EMERGENCY_HANDBOOK存放应急手册
                                BASE_DIR/HIGH_LEVEL_EVENT存放高等级事件
                                BASE_DIR/TRANSACTION_PATH存放交易路径
    :param file_types: 在views中有定义，用文件扩展名限制用户上传文件的类型
    :return: result{'key1':上传文件个数, 'code':code, 'specify_files/all_files':指定类型文件list/*文件类型list} 返回前端页面用户操作的结果
             code 101:未上传任何文件
             code 150:上传文件类型有问题(扩展名判断)
             code 100:上传成功
             code 199:其他未判断条件(可扩展优化：细化判断逻辑返回新的code)
    """
    # 限定扩展名file_types为 * 时，获取用户上传的所有文件列表
    all_files = []
    # 限定扩展名file_types为固定格式时，获取用户上传文件的列表
    specify_files = []
    result = {}
    # 如果用户未上传文件
    if len(files) == 0:
        result['code'] = '101'
    else:
        # 先对上传的文档进行格式检查，如果格式有误，不进行任何操作，直接报错退出
        for file in files:
            # 如果不要求上传格式，则跳过
            if file_types == ['*']:
                pass
            # 如果要求的上传格式
            elif file_types != ['*']:
                # 获取用户上传文件的扩展名，需要考虑文件名中包含'.'的情况，例如'abc.123.xls'  ！！！优化请尝试使用endwith
                file_type_user = file.name.split('.')[len(file.name.split('.')) - 1]
                # 用户上传文件的扩展名和系统指定的扩展名进行'不区分大小写'的对比，对比一致则跳过
                if file_type_user.lower() in [file_type.lower() for file_type in file_types]:
                    pass
                else:
                    # 用户上传文件的扩展名和系统指定的扩展名进行'不区分大小写'的对比，对比不一致则返回150
                    result['code'] = '150'
                    return result

        # 上传文件格式无问题，进行上传操作
        for file in files:
            # 给文件名称配一个唯一值
            time_now = timezone.now()  # 获取当前日期时间
            m = hashlib.md5()
            m.update(str(time_now).encode())  # 给当前时间编码
            time_now = m.hexdigest()

            all_files.extend([time_now + file.name])
            if os.path.exists(os.path.join(path)) is False:
                os.mkdir(os.path.join(path))
            f = open(os.path.join(path, time_now + file.name), 'wb+')  # 使用os.path.join()拼接路径，并打开文件

            # 文件写入指定目录
            for chunk in file.chunks():
                f.write(chunk)
            f.close()
            result['key1'] = len(all_files)
            result['code'] = '100'
            result['all_files'] = all_files
            print("code:", result['code'], "\t文件上传成功:\t\t\t\t\t", file.name)
    return result
