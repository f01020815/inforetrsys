# -*- coding:utf-8 -*- 
# Author: Li Gaoyang<gylia@isoftstone.com>
from adminworkstation.models import PathApproval
from adminworkstation.models import Path
from workstation.publicwork.user_detail import user_detail
from userworkstation.models import UploadFile
from mongoengine.queryset.visitor import Q


def DBupdate_pathid(path_id,request):
    # 获取更新人信息
    user = user_detail(request)
    # 更新记录时，在审批表插入更新前原始数据
    # 根据path_id获取Path表原始数据
    res = Path.objects.filter(path_id=path_id)

    # 原数据插入审批表PathApproval
    message = PathApproval()
    num = len(PathApproval.objects)
    new_approval_id = num + 1
    message.approval_id = new_approval_id

    message.approval_opt = "原数据"
    message.approval_o_path_id = str(path_id)
    message.approval_linetype = res[0].path_linetype
    message.approval_content = res[0].path_content
    message.approval_tradetype = res[0].path_tradetype
    message.approval_tradepath = res[0].path_tradepath
    message.approval_remark = res[0].path_remark
    # 查询原数据文档项,将pathid匹配的文档加入list里
    res_file_info = {}
    for res_file in UploadFile.objects.filter(Q(file_path_id=str(path_id)) & Q(file_show_state=1)):
        if res_file:
            file_id = res_file.file_id
            file_name = res_file.file_name[32:len(res_file.file_name)]
            file_info = {file_id: file_name}
            res_file_info.update(file_info)
    message.approval_o_file_info = str(res_file_info)

    message.approval_hostname = user[0]
    message.approval_ip = user[1]
    message.approval_mac = user[2]
    # message.approval_path_id_b = str(inserted_path_id)
    # 保存
    message.save()
