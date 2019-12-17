import jieba
import re
from InfoRetrSys.settings import samewords, basedata


def samewordslist(transaction_path):
    words_temp = jieba.cut(transaction_path, cut_all=False)
    result = " ".join(words_temp)
    sysnames = re.findall(r"[\w']+", result)
    # 获取字典中所有key并放入列表中

    res = []
    res_basedata = []
    for word in sysnames:
        if word in samewords:
            res.append(samewords[word])
            for tmp in basedata[samewords[word]]:
                if tmp.strip() !="" :
                    res_basedata.append(tmp.strip())
        else:
            res.append(word)
            res_basedata.append(word)
    return(res, res_basedata)
