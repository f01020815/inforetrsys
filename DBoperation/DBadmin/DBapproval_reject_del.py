# add by wangshibin 20190723
from adminworkstation.models import Path
from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile


def DBapproval_reject_del(approval_o_path_id, approval_id):
    # 审批：删除驳回
    Path.objects.filter(path_id=approval_o_path_id).update(path_show_state=1, path_approval_state=1)
    # 删除审批表
    PathApproval.objects.filter(approval_id=approval_id).delete()

