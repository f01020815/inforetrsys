# -*- coding:utf-8 -*-
# Author: Li Gaoyang<gylia@isoftstone.com>
from adminworkstation.models import Path
from adminworkstation.models import SysPath
from DBoperation.DBadmin.DBinsertSysPath import insert_syspath
from workstation.publicwork.stopwordslist import stopwordslist
from workstation.publicwork.samewordslist import samewordslist


def insert_to_syspath(path_id):
    """
    该函数的逻辑说明：
    1.获取路径条目
    2.分词
    3.去除符号
    4.插入表
    5.返回分词后的系统名称
    """
    for x in Path.objects.filter(path_id=path_id):
        # 从数据库中获取path表的路径字段
        transaction_path = x.path_tradepath

        # 将交易路径拆分成单独的系统名[sysnames]
        # 同义词和停用词过滤
        samewords,res_samewords = samewordslist(transaction_path)
        sysnames = stopwordslist(samewords)

        # 合并重复文字，并转化为字典
        syswords_dict = {}
        for l in sysnames:
            syswords_dict[l] = syswords_dict.get(l,0)+1

        # 遍历字典中的key，即系统名称。
        for sysname in syswords_dict:
            # 做Log使用的数据 包括['系统名称',path_id,'次数频率']
            data = []
            data.extend([sysname])
            data.extend([path_id])
            str_syaname = str(syswords_dict[sysname])
            data.extend(str_syaname)
            # 1、若系统名在SysPath中存在记录，则不操作
            if len(SysPath.objects.filter(syspath_name=data[0])) != 0:
                pass
            # 2、若系统名在SysPath中无记录，则插入该条记录
            else:
                insert_syspath(data)
    return syswords_dict
