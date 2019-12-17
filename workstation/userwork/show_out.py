# -*- coding:utf-8 -*-
# Author: Li Gaoyang<gylia@isoftstone.com>
import math   # 导入 math 模块
from adminworkstation.models import SysPath
from adminworkstation.models import PartWord
from workstation.publicwork.cut_words import cut_words
from DBoperation.DBuser.DBshow_work import DBshow_work


def show_out(inputs):
    res_samewords = []
    # 定义返回show.html的值:datas 和 搜索的关键字（用于标红）:key_words
    datas = []
    key_words_new = []
    X = {}
    Y = {}
    Y_sum = {}
    a = 0.7
    b = 1 - a

    # 将输入的内容转为大写的str格式
    words = ''.join(inputs).upper()

    # 1、如果输入内容为空
    if len(words) == 0 or words.isspace() or words.strip() == "":
        print("输入内容为空")
        datas = "null"
        key_words_new = "null"

    # 2、如果输入内容不为空
    else:
        # 进行jieba分词,返回字典
        key_words_old, res_samewords = cut_words(words)

        # 去除重复输入的字
        key_words_new = []
        for l in key_words_old:
            if l not in key_words_new:
                key_words_new.append(l)

        dict_temp = {}
        ds_num = 0
        dp_num = 0
        for key_word in key_words_new:
            # # 查找SysPath表生成字典dict_temp{'path_id1': 1, 'path_id2': 1, 'path_id3': 1}
             #dict_syspath ={}
            dict_partword = {}
            Y = {}
            # for x in SysPath.objects(syspath_name=key_word):
            #     syspath_str = x.syspath_list
            #     dict_syspath = eval(syspath_str)
            #     syspath_list = dict_syspath.keys()
            #     syspath_value = dict_syspath.values()
            #     for words_num in dict_syspath:
            #         if words_num not in Y:
            #             Y[words_num] = int(0)
            #
            #         Y[words_num] += (1.0 + math.log10(int(dict_syspath[words_num])))
            #         # Y[words_num] += (1 + 0.01 * int(dict_syspath[words_num]))
            #
            #     for m in syspath_list:
            #         if m in dict_temp:
            #             dict_temp[m] += 1
            #         else:
            #             dict_temp[m] = int(1)


            # 查找PartWord表生成字典并添加进dict_temp{'path_id1': 2, 'path_id2': 1, 'path_id3': 2, 'path_id7': 1}
            for x in PartWord.objects(partword_name=key_word):
                partword_str = x.partword_list
                dict_partword = eval(partword_str)
                partword_list = dict_partword.keys()
                partword_valuet = dict_partword.values()
                for words_num in dict_partword:
                    if words_num not in Y:
                        Y[words_num] = int(0)

                    Y[words_num] += (1.0 + math.log10(int(dict_partword[words_num])))
                    # Y[words_num] += (1 + 0.01*int(dict_partword[words_num]))


                for n in partword_list:
                    if n in dict_temp:
                        dict_temp[n] += 1
                    else:
                        dict_temp[n] = int(1)

            for y_tmp in Y:
                ds_tmp = 0
                dp_tmp = 0
                # if y_tmp in dict_syspath:
                #     ds_tmp = float(dict_syspath[y_tmp])
                if y_tmp in dict_partword:
                    dp_tmp = float(dict_partword[y_tmp])
                if y_tmp not in Y_sum:
                    Y_sum[y_tmp] = 0

                if (ds_tmp + dp_tmp) != 0:
                    Y_sum[y_tmp] += b * (Y[y_tmp] /len(key_words_new))
                    # Y_sum[y_tmp] += b * (Y[y_tmp] / (ds_tmp + dp_tmp))

        # 2.1、如果查询结果为空
        if len(dict_temp) == 0:
            print("索引表未找到匹配项")
            datas = "null"
            key_words_new = "null"

        # 2.2、如果查询结果不为空
        else:
        # x = dict_temp.values()

            Z = {}
            for tmp in dict_temp:
                X[tmp] = a * dict_temp[tmp] / (2 * len(key_words_new))
                Z[tmp] = X[tmp]+Y_sum[tmp]


            # 对字典dict_temp的值进行降序排序放入dict_all[('path_id1': 2), ('path_id3': 2), ('path_id2': 1), ('path_id7': 1)]
            dict_all = sorted(Z.items(), key=lambda z: z[1], reverse=True)
            # 从Path表中取值
            for n in range(len(dict_all)):
                path_id = int(dict_all[n][0])
                data = DBshow_work(path_id)
                if len(data) != 0:
                    datas.append(data)

    return datas, res_samewords
