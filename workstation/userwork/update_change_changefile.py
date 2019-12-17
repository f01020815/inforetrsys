from workstation.publicwork.upload_high_file import upload_high_file
from DBoperation.DBuser.DBinsert_pathid import DBinsert_pathid
from adminworkstation.models import Path
from workstation.publicwork.user_detail import user_detail
from adminworkstation.models import PathApproval
from django.contrib import messages
from userworkstation.models import UploadFile
from workstation.publicwork.html_to_path import html_to_path
from workstation.publicwork.log_record import normal

def update_change_changefile(path_id, approval_n_list, approval_o_list, request, upload_files, source):
    # 插入审批表 作为修改数据 new_approval_id_n是修改的审批ID
    data_source = [approval_n_list[0], approval_n_list[1], approval_n_list[2], approval_n_list[3], approval_n_list[4]]
    new_path_id, new_approval_id_n = html_to_path(request, data_source, source)
    # 将opt'增加'改为'修改'
    PathApproval.objects.filter(approval_id=new_approval_id_n).update(approval_opt="修改")

    # 审批表插入 作为原数据 new_approval_id_o 是原数据的审批ID
    data = []
    data.append(approval_o_list[0])
    data.append(approval_o_list[1])
    data.append(approval_o_list[2])
    data.append(approval_o_list[3])
    data.append(approval_o_list[4])
    data.extend(user_detail(request))
    new_approval_id_o = DBinsert_pathid(data, path_id)
    PathApproval.objects.filter(approval_id=new_approval_id_o).update(approval_opt="原数据")
    # 更新审批表原数据的file信息
    approval_o_file_info = {}
    if approval_o_list[6]:
        for file_id in approval_o_list[6]:
            res = UploadFile.objects.filter(file_id=file_id)
            res[0].file_name
            file_info = {file_id: res[0].file_name[32:len(res[0].file_name)]}
            approval_o_file_info.update(file_info)
    PathApproval.objects.filter(approval_id=new_approval_id_o).update(approval_o_file_info=str(approval_o_file_info))
    # 删除的文档不显示
    if approval_o_list[6] != approval_n_list[6]:
        del_file_lists = list(set(approval_o_list[6]) - set(approval_n_list[6]))
        file_names = []
        for del_file_list in del_file_lists:
            UploadFile.objects.filter(file_id=del_file_list).update(file_show_state=0)
            filename = UploadFile.objects.filter(file_id=del_file_list)
            file_names.append(filename[0].file_name)
        normal(request, '删除文件', file_names, path_id)

     # 上传文档并插入UploadFile表记录
    if upload_files:
        approval_file_info = upload_high_file(new_path_id, upload_files, request)
        # 更新审批表修改数据的approval_n_file_info信息
        PathApproval.objects.filter(approval_id=new_approval_id_n).update(approval_n_file_info=str(approval_file_info))
    # 已有文档
    approval_o_file_info = {}
    if approval_n_list[6]:
        for file_id in approval_n_list[6]:
            res = UploadFile.objects.filter(file_id=file_id)
            res[0].file_name
            # 将文档更新到新path_id上
            UploadFile.objects.filter(file_id=file_id).update(file_path_id=str(new_path_id))
            file_info = {file_id: res[0].file_name[32:len(res[0].file_name)]}
            approval_o_file_info.update(file_info)
    PathApproval.objects.filter(approval_id=new_approval_id_n).update(approval_o_file_info=str(approval_o_file_info))

    # 将原条目设置为不显示，审批中，无法更新
    Path.objects.filter(path_id=str(path_id)).update(path_show_state=0, path_approval_state=0)
    data.remove(data[5])
    data.remove(data[5])
    data.remove(data[5])
    normal(request, '删除', data, path_id)
    new_address = ("/update/?path_id=" + str(new_path_id))
    messages.success(request, "更新成功!")
    return new_address
