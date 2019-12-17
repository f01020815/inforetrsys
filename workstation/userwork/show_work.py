# add by wangshibin 20190718
import jieba
from workstation.publicwork.public_fenci import public_fenci
from workstation.userwork.show_work_list import show_work_list
jieba.load_userdict("userdict.txt")

def show_work(inputs):
    # 将输入的内容转为str形式
    words = ''.join(inputs[0].upper())
    # 进行jieba分词,返回字典
    res_words = public_fenci(words)
    # 如果输入内容为空
    if len(words) == 0:
        res_db_all ="null"
        res_words ="null"
        return res_db_all, res_words
    # 如果输入内容为空
    elif words.isspace() or words.strip() == "":
        res_db_all ="null"
        res_words ="null"
        return res_db_all, res_words
    else:
    # 如果符合要求
        res_db_all = show_work_list(res_words)
        return res_db_all, res_words
