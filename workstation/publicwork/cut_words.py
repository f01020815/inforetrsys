# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
from workstation.publicwork.stopwordslist import stopwordslist
from workstation.publicwork.samewordslist import samewordslist


def cut_words(words):
    """
    :param words: 要分词的字符串，type(words) : str
    :return: 按照词性拆分后，返回词性是'v' or 's' or '*n*'的list
    """
    #key_words = []
    #words_temp = jieba.posseg.cut(words)
    new_words = words.replace(" ", "")
    samewords,res_samewords = samewordslist(new_words)
    words_temp = stopwordslist(samewords)
    #words_temp = jieba.cut(words_temps, cut_all=True)
    #
    # # 将分词word和词性flag放入列表     eg:words['现金', 'n', '转账', 'v']
    # words = []
    # for y in cut_words:
    #     words.extend([y.word, y.flag])
    #
    # for z in range(1, len(words), 2):
    #     if words[z] == 'n' or words[z] == 'v' or words[z] == 's':
    #         key_word = words[z-1]
    #
    result = " ".join(words_temp)
    key_words = result.split(' ')
    #res_samewordsw为标红所用
    return key_words,res_samewords
