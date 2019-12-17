# add by wangshibin 20190724
from adminworkstation.models import Path
from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile

def DBapproval_agree_ins(approval_o_path_id, approval_id):
    # 审批：增加同意
    Path.objects.filter(path_id=approval_o_path_id).update(path_show_state=1, path_approval_state=1)
    # 通过审批表查询审批的文档ID
    # res = PathApproval.objects.filter(approval_id=approval_id)
    # res_file = res[0].approval_n_file_info
    # if res_file:
    #     dict_res_file = eval(res_file)
    #     file_lists = dict_res_file.keys()
    #     for file_list in file_lists:
    #         file_id = file_list
    #     # 文档显示
    #     UploadFile.objects.filter(file_id=int(file_id)).update(file_show_state=1)
    # 删除审批表内容
    PathApproval.objects.filter(approval_id=approval_id).delete()
