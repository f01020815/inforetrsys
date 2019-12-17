# add by wangshibin 20190724
from adminworkstation.models import PathApproval

def DBinsert_pathid(data, inserted_path_id):
    # 增加条目，待审批
    # 插入到审批表中
    message = PathApproval()
    num = len(PathApproval.objects)
    new_approval_id = num + 1
    message.approval_id = new_approval_id

    message.approval_opt = "增加"
    message.approval_o_path_id = str(inserted_path_id)
    message.approval_linetype = data[0]
    message.approval_content = data[1]
    message.approval_tradetype = data[2]
    message.approval_tradepath = data[3]
    message.approval_remark = data[4]
    message.approval_hostname = data[5]
    message.approval_ip = data[6]
    message.approval_mac = data[7]
    message.approval_path_id_b = str(inserted_path_id)

    # 保存
    message.save()
    return new_approval_id
