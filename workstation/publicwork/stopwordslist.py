from InfoRetrSys.settings import stopwords


def stopwordslist(samewords):
    sysnames = []
    for sys_word in samewords:
        if sys_word not in stopwords:
            if sys_word != '\t':
                sysnames.append(sys_word)
    return sysnames
