from adminworkstation.models import Path
from userworkstation.models import UploadFile

def update_get_old_list(path_id):
    # 获取旧数据的 连接类型 / 交易描述 / 交易类型 / 交易路径 / 备注说明  /hash
    res = Path.objects.filter(path_id=path_id)
    data_source = [res[0].path_linetype,
    res[0].path_content,
    res[0].path_tradetype,
    res[0].path_tradepath,
    res[0].path_remark,
    res[0].path_hash]

    # 查找文档ID
    file_list_db = []
    for UploadFiles in UploadFile.objects(file_path_id=path_id):
        file_list_db.append(UploadFiles.file_id)

    # 排序
    file_list_db.sort()
    # 加入到总列表中
    data_source.append(file_list_db)
    return data_source
