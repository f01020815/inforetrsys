# add by wangshibin 20190720
import re


def show_dict_addwork(res_dict_all, syspath_list):
    new_list = re.split(",", syspath_list)
    res_dict = {}
    for l in new_list:
        res_dict[l] = int(1)

    # 加入到字典res_dict_all
    for key in res_dict_all:
        if res_dict.get(key):
            res_dict_all[key] = res_dict_all[key] + res_dict[key]
        else:
            res_dict_all[key] = res_dict_all[key]
    for key in res_dict:
        if res_dict_all.get(key):
            pass
        else:
            res_dict_all[key] = res_dict[key]
    return res_dict_all
