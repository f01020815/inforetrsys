# add by wangshibin 20190720
from adminworkstation.models import SysPath
from adminworkstation.models import PartWord
from workstation.userwork.show_dict_addwork import show_dict_addwork


def show_words_dict(res_words):
    res_dict_all = {}
    for key in res_words:
        # 查找SysPaths表
        for SysPaths in SysPath.objects(syspath_name=key):
            syspath_list = SysPaths.syspath_list
            show_dict_addwork(res_dict_all, syspath_list)

        # 查找PartWords表
        for PartWords in PartWord.objects(partword_name=key):
            partword_list = PartWords.partword_list
            show_dict_addwork(res_dict_all, partword_list)
    # 排序
    if res_dict_all:
        #res_list_all = res_dict_all.keys()
        #res_list_all.sort(key=res_dict_all.__getitem__, reverse=False)
        res_dict_all = sorted(res_dict_all.items(), key=lambda x: x[1], reverse=True)
    else:
        res_dict_all = "null"
    return res_dict_all
