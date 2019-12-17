# add by wangshibin 20190724
from adminworkstation.models import Path
from adminworkstation.models import PathApproval
from userworkstation.models import UploadFile

def DBapproval_reject_ins(approval_o_path_id, approval_id):
    # 审批：增加驳回
    Path.objects.filter(path_id=approval_o_path_id).update(path_show_state=0, path_approval_state=1)
    Path.objects.filter(path_id=approval_o_path_id).update(path_hash="")
    UploadFile.objects.filter(file_path_id=approval_o_path_id).update(file_show_state=0, file_path_id="")
    PathApproval.objects.filter(approval_id=approval_id).delete()
