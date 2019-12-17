# add by wangshibin 20190723
from adminworkstation.models import Path
from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile

def DBapproval_agree_del(approval_o_path_id, approval_id):
    # 审批：删除同意
    Path.objects.filter(path_id=approval_o_path_id).update(path_show_state=0, path_approval_state=1)
    Path.objects.filter(path_id=approval_o_path_id).update(path_hash="")

    # 通过审批表 查询到删除的path关联的文档
    res = PathApproval.objects.filter(approval_id=approval_id)
    res_file = res[0].approval_o_file_info
    if res_file:
        dict_res_file = eval(res_file)
        file_lists = dict_res_file.keys()
        for file_list in file_lists:
            file_id = file_list
            # 文档不显示
            UploadFile.objects.filter(file_id=file_id).update(file_show_state=0, file_path_id="")
    # 删除审批表
    PathApproval.objects.filter(approval_id=approval_id).delete()

