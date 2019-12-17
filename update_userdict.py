# 将samewords.txt同步到userdict.txt上
import codecs

# 读取文件
with codecs.open("./samewords.txt", "r", encoding='utf-8-sig') as f:
    text = f.read()
    all_word = text.strip().split()
# 追加字符
for word in all_word:
    res_word = word + " 8888888 n"
    #写入文件
    f = open("./userdict.txt", "a", encoding='utf-8-sig')
    f.write('\r\n'+res_word)
    print(res_word)
f.close()