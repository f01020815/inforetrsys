from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile
from adminworkstation.models import Path
from workstation.publicwork.log_record import normal
from workstation.publicwork.user_detail import user_detail


def DBdelete_fileid(request, file_id):
    # 根据file_id获取该记录对应Path表中的path_id(也就是UploadFile中的file_path_id字段)
    x = UploadFile.objects.filter(file_id=file_id)
    path_id = x[0].file_path_id
    # 加入到审批表
    message = PathApproval()
    num = len(PathApproval.objects)
    new_approval_id = num + 1
    message.approval_id = new_approval_id

    hostname_ip_mac = user_detail(request)
    res = Path.objects.filter(path_id=path_id)
    message.approval_opt = "删除文档"
    message.approval_o_path_id = path_id
    message.approval_linetype = res[0].path_linetype
    message.approval_content = res[0].path_content
    message.approval_tradetype = res[0].path_tradetype
    message.approval_tradepath = res[0].path_tradepath
    message.approval_remark = res[0].path_remark
    message.approval_hostname = hostname_ip_mac[0]
    message.approval_ip = hostname_ip_mac[1]
    message.approval_mac = hostname_ip_mac[2]
    message.approval_path_id_b = path_id
    message.save()

    # 将删除的文档加入list里
    res_file_info = {}
    res = UploadFile.objects.filter(file_id=int(file_id))
    file_name = res[0].file_name[32:len(res[0].file_name)]
    file_info = {file_id: file_name}
    res_file_info.update(file_info)
    PathApproval.objects.filter(approval_id=int(new_approval_id)).update(approval_file_info=str(res_file_info))

    # 不显示旧文档
    UploadFile.objects.filter(file_id=int(file_id)).update(file_show_state=0, file_approval_state=0)
    # 重定向网址
    new_url = ("/update/?path_id=" + str(x[0].file_path_id))
    normal(request, '删除文件', file_name, 0)
    return new_url
