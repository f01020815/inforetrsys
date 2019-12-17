# add by wangshibin 20190718
import jieba
import sys
import jieba.posseg as pseg
jieba.load_userdict("userdict.txt")


def public_fenci(words):
    fenci_words = pseg.cut(words)
    # 创建字典
    dict_words = {}
    for w in fenci_words:
        dict_words.update({w.word: w.flag})
    # 获取分词后的n和v词性（过滤），
    res_dict_words = filter(lambda x: 'n' in x[1] or x[1] == 'v' or x[1] == 's', dict_words.items())
    # 以列表形式返回key值
    res_dict_words = dict(res_dict_words)
    res_words = list(res_dict_words.keys())
    return res_words
