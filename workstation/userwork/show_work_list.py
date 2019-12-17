# add by wangshibin 20190718
from workstation.userwork.show_words_dict import show_words_dict
from workstation.userwork.show_db_list import show_db_list

def show_work_list(res_words):
    # 在SysPath和PartWord表中搜索, 返回排序后的字典
    res_dict_all = show_words_dict(res_words)
    # 如果查询结果为空格则直接返回，如果有值则返回数据库的查询结果
    if res_dict_all == "null":
        res_db_all ="null"
        return res_db_all
    else:
        res_db_all = show_db_list(res_dict_all)
        return res_db_all
