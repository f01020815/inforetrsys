from adminworkstation.models import Path

# add by wangshibin 20190725
def DBuptdate_find_data(path_id):
    # 获取详细信息
    res = Path.objects.filter(path_id=path_id)
    line_type = res[0].path_linetype
    content = res[0].path_content
    trade_type = res[0].path_tradetype
    trade_path = res[0].path_tradepath
    remark = res[0].path_remark
    state = res[0].path_approval_state
    return line_type, content, trade_type, trade_path, remark, state
