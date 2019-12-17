from adminworkstation.models import Path
from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile
from mongoengine.queryset.visitor import Q


# add by wangshibin 20190723
def DBapproval_agree_update(new_path_id, new_approval_id):
    # 旧path_id不显示
    res = PathApproval.objects.filter(approval_id=int(new_approval_id)+1)
    old_path_id = res[0].approval_o_path_id
    Path.objects.filter(path_id=int(old_path_id)).update(path_show_state=0, path_approval_state=1)

    # 如果审批时存在原数据，则删除原数据的hash值
    result = PathApproval.objects.filter(approval_id=int(new_approval_id))
    result_old = PathApproval.objects.filter(approval_id=int(new_approval_id) + 1)
    if int(result[0].approval_o_path_id) != int(result_old[0].approval_o_path_id):
        Path.objects.filter(path_id=int(result_old[0].approval_path_id_b)).update(path_hash="")

    # 新path_id显示
    Path.objects.filter(path_id=new_path_id).update(path_show_state=1, path_approval_state=1)

    # 获取删除的文档，删除文档
    UploadFile.objects.filter(Q(file_path_id=old_path_id) & Q(file_show_state=0)).update(file_path_id="")

    # 删除path_approval表
    PathApproval.objects.filter(approval_id=new_approval_id).delete()
    PathApproval.objects.filter(approval_id=int(new_approval_id)+1).delete()

