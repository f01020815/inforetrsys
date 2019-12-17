from userworkstation.models import UploadFile
from mongoengine.queryset.visitor import Q
from adminworkstation.models import Path


# add by wangshibin 20190725
def DBuptdate_find_upload_file(path_id):
    # 获取详细信息
    get_reports_titles = []
    for upload_files in UploadFile.objects(Q(file_path_id=path_id) & Q(file_show_state="1")):
        res = []
        res.append(upload_files.file_name[32:len(upload_files.file_name)])
        res.append(upload_files.file_id)

        ress = Path.objects.filter(path_id=path_id)
        res.append(ress[0].path_approval_state)

        res.append(upload_files.file_path)
        get_reports_titles.append(res)
    return get_reports_titles

