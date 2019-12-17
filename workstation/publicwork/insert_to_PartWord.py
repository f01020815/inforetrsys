# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
from adminworkstation.models import Path
from adminworkstation.models import PartWord
from DBoperation.DBadmin.DBinsertPartWord import insert_pathword
from workstation.publicwork.cut_words import cut_words
from collections import Counter

def insert_to_partword(path_id, syswords_dict):
    """
    该函数的逻辑说明：根据path_id查询Path表得到transaction_path，拆分成单个系统名sysname，将sysname和path_id写入SysPath索引表
    :param path_id: 每插入一条新数据到Path表后，返回所插入数据的path_id
    :return:
    """
    for x in Path.objects.filter(path_id=path_id):
        # 此处根据path_id在Path表里只会匹配到一条记录；若匹配多条记录需extend成list处理，或在for下写处理过程
        connection_type = x.path_linetype
        transaction_description = x.path_content
        transaction_type = x.path_tradetype
        remark = x.path_remark

        all_words = connection_type+" "+transaction_description+" "+transaction_type+" "+remark
        # 同义词和停用词过滤
        key_words,res_samewords = cut_words(all_words)
        # 合并重复文字，并转化为字典
        samewords_dicts = {}
        for l in key_words:
            samewords_dicts[l] = samewords_dicts.get(l, 0) + 1

        #合并关键字字典和系统名称字典
        X, Y = Counter(samewords_dicts), Counter(syswords_dict)
        samewords_dict = dict(X + Y)

        # 遍历字典中的key，即关键字。
        for key_word in samewords_dict:
            data = []
            data.extend([key_word])
            data.extend([path_id])
            str_words = [samewords_dict[key_word]]
            data.extend(str_words)

            # 1、若关键字在PartWord中存在记录，则更累加新该记录的partword_list
            if len(PartWord.objects.filter(partword_name=data[0])) != 0:
                for y in PartWord.objects.filter(partword_name=data[0]):
                    # 获取数据库中的syspath_list
                    partword_lists = y.partword_list
                    # 转化为字典模式
                    dict_partword_lists = eval(partword_lists)
                # 1.1、关键字在PartWord索引表存在，但对应的path_id未记录
                if str(data[1]) not in dict_partword_lists.keys():
                    dict_partword_lists.update({data[1]: data[2]})
                    # 更新记录
                    PartWord.objects.filter(partword_name=data[0]).update(partword_list=str(dict_partword_lists))
                    print("PartWord索引表 更新了 一条记录：关键字:%s， path_id:%d" % (data[0], data[1]))

                # 1.2、关键字和path_id均在PartWord索引表中存在，不做操作
                else:
                    print("PartWord索引表 已存在 该条记录：关键字:%s， path_id:%d" % (data[0], data[1]))

            # 2、若关键字在PartWord中无记录，则插入该条记录
            else:
                insert_pathword(data)
                print("PartWord索引表 新增了 一条记录：关键字:%s， path_id:%d" % (data[0], data[1]))

    return
