# add by wangshibin 20190723

from adminworkstation.models import Path

def insert_path(request, data):
    message = Path()
    num = len(Path.objects)
    # message.path_id = num+1
    new_path_id = num + 1
    message.path_id = new_path_id

    # 存储数据data[connection_type, transaction_description, transaction_type, transaction_path, \
    # remark, hostname, ip, mac, display_states, approval_states, execl_hash]
    message.path_linetype = data[0]
    message.path_content = data[1]
    message.path_tradetype = data[2]
    message.path_tradepath = data[3]
    message.path_remark = data[4]
    message.path_hostname = data[5]
    message.path_ip = data[6]
    message.path_mac = data[7]
    message.path_show_state = data[8]
    message.path_approval_state = data[9]
    message.path_hash = data[10]

    # 保存
    message.save()
    return new_path_id
