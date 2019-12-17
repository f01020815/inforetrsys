from DBoperation.DBuser.DBinsert_upload_file import insert_upload_file
from workstation.publicwork.user_detail import user_detail
from workstation.publicwork.upload_file import upload_file
from workstation.publicwork.log_record import normal


def upload_high_file(path_id, upload_files, request):
    # 高等级事件文档上传
    path = 'HIGH_LEVEL_EVENT\\' + str(path_id)
    file_types = ['DOCX']

    # 上传文件
    result = upload_file(upload_files, path, file_types)

    approval_file_info = {}
    # 插入数据库 高等级事件表
    for file in result['all_files']:
        data = []
        data.extend([path_id])
        data.extend([path])
        data.extend(user_detail(request))
        data.extend([file])
        # 插入数据库
        approval_n_file_infos = insert_upload_file(data)
        approval_file_info.update(approval_n_file_infos)
        #str6 = "】【".join(inser_file)
        normal(request, '上传文件', file, str(path_id))
    return approval_file_info
