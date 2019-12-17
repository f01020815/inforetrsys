# add by wangshibin 20190720
from adminworkstation.models import Path
from mongoengine.queryset.visitor import Q
from userworkstation.models import UploadFile

def DBshow_work(num):
    # 查询数据库中的表数据，返回索引结果
    res_list = []
    for res in Path.objects.filter((Q(path_id=num) & Q(path_show_state=1))):
        res_list.append(res.path_linetype)
        res_list.append(res.path_content)
        res_list.append(res.path_tradetype)
        res_list.append(res.path_tradepath)
        res_list.append(res.path_remark)
        #res_list.append(res.path_update_time)
        # 将pathid匹配的文档加入list里
        res_file_info = ""
        i = 1
        for res_file in UploadFile.objects.filter(Q(file_path_id=str(num)) & Q(file_show_state=1)):
            file_id = res_file.file_id
            file_name = res_file.file_name[32:len(res_file.file_name)]
            res_file_info += " <a href=""/document_show/?file_id=" + str(
                file_id) + " target=""_blank"" rel=""nofollow noopener noreferrer"" title=" + file_name + ">报告" + str(
                i) + "</a>"
            i = i + 1
        res_list.append(res_file_info)
        res_list.append(res.path_last_time)
        res_list.append(res.path_id)
        res_list.append(res.path_approval_state)
    return res_list

