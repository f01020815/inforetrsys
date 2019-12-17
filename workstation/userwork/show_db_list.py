# add by wangshibin 20190720
from DBoperation.DBuser.DBshow_work import DBshow_work


def show_db_list(res_dict_all):
    res_db_all = []
    for key in res_dict_all:
        num = str(key).split("'")[1]
        # 在path里查找所需要的所有结果
        res = DBshow_work(num)
        # 将结果加入列表
        if res:
            res_db_all.append(res)
    return res_db_all
