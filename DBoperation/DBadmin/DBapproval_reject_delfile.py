from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile


def DBapproval_reject_delfile(approval_o_path_id, approval_id):
    # 审批：删除驳回
    # 通过审批ID获取文档ID
    res = PathApproval.objects.filter(approval_id=approval_id)
    res_file = res[0].approval_file_info
    dict_res_file = eval(res_file)
    file_lists = dict_res_file.keys()
    for file_list in file_lists:
        file_id = file_list
        # 文档不显示
        UploadFile.objects.filter(file_id=file_id).update(file_show_state=1, file_approval_state=1)
    # 删除审批表内容
    PathApproval.objects.filter(approval_id=approval_id).delete()
