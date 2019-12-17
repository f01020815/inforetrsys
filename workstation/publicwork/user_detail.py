# -*- coding:utf-8 -*-
# Author: Li Gaoyang<gylia@isoftstone.com>
import socket
import uuid


def user_detail(request):
    # 获取访问用户的主机名
    hostname = socket.gethostname()

    # 获取访问用户的IP---使用request.META['REMOTE_ADDR']
    # print("feedback/work/user_detail的print:\n", request.META)
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    # ip = socket.gethostbyname(hostname)????????????????????????????使用哪种????????????????????????

    # 获取访问用户的MAC地址
    addr_num = hex(uuid.getnode())[2:]
    mac = "-".join(addr_num[i: i + 2] for i in range(0, len(addr_num), 2))

    hostname_ip_mac = [hostname, ip, mac]
    return hostname_ip_mac
