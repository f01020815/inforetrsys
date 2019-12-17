import hashlib


def update_get_new_list(request,ajax_file_list):
    # 获取用户更新的连接类型 / 交易描述 / 交易类型 / 交易路径 / 备注说明 放入data_source列表
    data_source = [request.POST.get('line_type'),
                   request.POST.get('content'),
                   request.POST.get('trade_type'),
                   request.POST.get('trade_path'),
                   request.POST.get('remark')]

    data_source_upper = []
    # 对数据源所有字母进行大写转换，并将数据拼接为data_source_upper[]
    for m in range(len(data_source)):
        data_source_upper.extend([data_source[m].upper()])

    # 将用户输入的信息计算md5 hash值
    hash_str = str(
        data_source_upper[0] + data_source_upper[1] + data_source_upper[2] + data_source_upper[3] + data_source_upper[
            4])
    object_md5 = hashlib.md5()
    object_md5.update(hash_str.encode(encoding='utf-8'))
    hash_value = object_md5.hexdigest()
    data_source.append(hash_value)

    # 对ajax排序 去除引号 排序
    if ajax_file_list == []:
        data_source.append(ajax_file_list)
    else:
        ajax_file_list = [int(x) for x in ajax_file_list]
        ajax_file_list.sort()
        data_source.append(ajax_file_list)
    return data_source
