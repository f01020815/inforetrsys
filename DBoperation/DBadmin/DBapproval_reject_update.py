from adminworkstation.models import Path
from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile
# add by wangshibin 20190723


def DBapproval_reject_update(new_path_id, new_approval_id):
    # 拒绝更新
    # 新path_id不显示
    Path.objects.filter(path_id=new_path_id).update(path_show_state=0, path_approval_state=1)
    # 旧path_id显示
    res = PathApproval.objects.filter(approval_id=int(new_approval_id) + 1)
    old_path_id = res[0].approval_o_path_id
    Path.objects.filter(path_id=int(old_path_id)).update(path_show_state=1, path_approval_state=1)

    # 如果审批时存在原数据，则删除新数据的hash值
    result = PathApproval.objects.filter(approval_id=int(new_approval_id))
    result_old = PathApproval.objects.filter(approval_id=int(new_approval_id)+1)
    if int(result[0].approval_o_path_id) != int(result_old[0].approval_o_path_id):
        Path.objects.filter(path_id=int(result[0].approval_o_path_id)).update(path_hash="")

    # 旧文档显示
    res = PathApproval.objects.filter(approval_id=int(new_approval_id)+1)
    res_o_file = res[0].approval_o_file_info
    if res_o_file:
        res_file_o_lists = eval(res_o_file)
        for res_file_o_lis in res_file_o_lists:
            # 将文档回归到旧path_id
            UploadFile.objects.filter(file_id=res_file_o_lis).update(file_path_id=old_path_id)
            # 显示
            UploadFile.objects.filter(file_id=res_file_o_lis).update(file_show_state=1)

    #  删除新增的文档
    ress = PathApproval.objects.filter(approval_id=int(new_approval_id))
    res_n_file = ress[0].approval_n_file_info
    if res_n_file:
        res_file_n_lists = eval(res_n_file)
        for res_file_n_lis in res_file_n_lists:
            UploadFile.objects.filter(file_id=res_file_n_lis).update(file_show_state=0,  file_path_id="")

    # 删除path_approval表
    PathApproval.objects.filter(approval_id=int(new_approval_id)).delete()
    PathApproval.objects.filter(approval_id=int(new_approval_id)+1).delete()
