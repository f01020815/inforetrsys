# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>


def insert_table(class_name, words, values):
    """
    :param class_name: 在DBoperation中定义的class，
                       在使用该函数前必须import对应的class！eg: from adminworkstation.models import class_name
    :param words: file_type:list，models.class中的字段，表中的域，要插入的域；实现方法是将数据插入数据库表的list[n]域中
    :param values: file_type:list，从execl获取或者前段页面获取的值；实现方法是将list[n]数据插入数据库的表中
    :return: result{'key1': true/false, 'code':code}返回前端页面用户操作的结果；key1作为调用该函数后判断是否继续执行的依据，code返回码有助于排错,打印log用来优化
            code 300:数据插入成功
            code 399:数据插入失败，其他未判断条件(可扩展优化：细化判断逻辑返回新的code)
    """
    try:
        if len(words) != len(values):
            result = {'code': 310}
            print("插入数据的列数和定义插入表的域的数量不匹配，code:", result['code'])
        else:
            table = class_name()
            for i in range(0, len(words)):
                table.words[i] = values[i]
                table.save()
            result = {'key1': 'true', 'code': 300}
            print("数据插入成功，code:", result['code'])
    except Exception as error:
        result = {'key1': 'false', 'code': 399}
        print("系统提示:", error)
        print("数据插入失败，code:", result['code'])

    return result
