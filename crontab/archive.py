# 归档日志文件

# 创建本月目录
import time
import os,shutil

# 获取当前时间
localtime = time.strftime('%Y-%m',time.localtime(time.time()))

# 目录
old_file_dir = r'..\LOG'
new_file_dir = old_file_dir + str('\\' + localtime)

# 如果目录不存在 则创建目录
if os.path.exists(new_file_dir) is False:
        os.makedirs(new_file_dir)

# 文件归档
old_file_list = os.walk(old_file_dir)
for path, dirs, filelist in old_file_list:
    for filename in filelist:
        if 'log.'+ localtime in filename:
            full_path = os.path.join(path, filename)  # 旧地址 + 文件名
            despath = new_file_dir + '\\'+filename  # 新地址 +文件名
            shutil.move(full_path, despath)
