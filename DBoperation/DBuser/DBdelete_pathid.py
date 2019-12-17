# add by wangshibin 20190723
from adminworkstation.models import Path
from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile
from mongoengine.queryset.visitor import Q

def delete_pathid_work(path_id, request):
    # 删除条目，待审批
    # 更新Path表审批状态
    Path.objects.filter(path_id=path_id).update(path_show_state=0, path_approval_state=0)
    # 获取Path信息
    res = Path.objects.filter(path_id=path_id)
    # 插入到审批表中
    message = PathApproval()
    num = len(PathApproval.objects)
    new_approval_id = num + 1
    message.approval_id = new_approval_id

    message.approval_opt = "删除"
    message.approval_o_path_id = path_id
    message.approval_linetype =res[0].path_linetype
    message.approval_content =res[0].path_content
    message.approval_tradetype =res[0].path_tradetype
    message.approval_tradepath =res[0].path_tradepath
    message.approval_remark =res[0].path_remark
    message.approval_hostname = request[0]
    message.approval_ip = request[1]
    message.approval_mac = request[2]
    message.approval_path_id_b = path_id
    # 将pathid匹配的文档加入list里
    res_file_info = {}
    for res_file in UploadFile.objects.filter(Q(file_path_id=str(path_id)) & Q(file_show_state=1)):
        if res_file:
            file_id = res_file.file_id
            file_name = res_file.file_name[32:len(res_file.file_name)]
            file_info = {file_id:file_name}
            res_file_info.update(file_info)
    message.approval_o_file_info = str(res_file_info)
    # 保存
    message.save()
