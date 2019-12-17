# add by wangshibin 20190723
from adminworkstation.models import PathApproval
from mongoengine.queryset.visitor import Q


def DBapproval_find_add_del(user):
    # 查询所有增加和删除的待审批的条目
    approval_list_add_del = []
    if user == "admin":
        for res in PathApproval.objects.filter(Q(approval_opt="增加") | Q(approval_opt="删除")):
            approval_list= []
            approval_list.append(res.approval_opt)
            approval_list.append(res.approval_linetype)
            approval_list.append(res.approval_content)
            approval_list.append(res.approval_tradetype)
            approval_list.append(res.approval_tradepath)
            approval_list.append(res.approval_remark)
            #approval_list.append(eval(res.approval_file_info))
            i = 1
            if res.approval_n_file_info:
                res_file_info = ""
                for key, value in eval(res.approval_n_file_info).items():
                    res_file_info += " <a href=""/document_show/?file_id="+str(key)+" target=""_blank"" rel=""nofollow noopener noreferrer"" title="+value+">报告"+str(i)+"</a>"
                    i=i+1
                approval_list.append(res_file_info)
            elif res.approval_o_file_info:
                res_file_infos = ""
                for key, value in eval(res.approval_o_file_info).items():
                   res_file_infos += " <a href=""/document_show/?file_id="+str(key)+" target=""_blank"" rel=""nofollow noopener noreferrer"" title="+value+">报告"+str(i)+"</a>"
                   i = i + 1
                approval_list.append(res_file_infos)
            else:
                res_file_infoss = ""
                approval_list.append(res_file_infoss)
            approval_list.append(res.approval_time)
            approval_list.append(res.approval_ip)
            approval_list.append(res.approval_o_path_id)
            approval_list.append(res.approval_id)
            approval_list_add_del.append(approval_list)

    else:
        for res in PathApproval.objects.filter(Q(approval_hostname=user[0]) & Q(approval_ip=user[1]) & Q(approval_mac=user[2])).filter(Q(approval_opt="增加") | Q(approval_opt="删除")):
            approval_list = []
            approval_list.append(res.approval_opt)
            approval_list.append(res.approval_linetype)
            approval_list.append(res.approval_content)
            approval_list.append(res.approval_tradetype)
            approval_list.append(res.approval_tradepath)
            approval_list.append(res.approval_remark)
            # approval_list.append(eval(res.approval_file_info))
            i = 1
            if res.approval_n_file_info:
                res_file_info = ""
                for key, value in eval(res.approval_n_file_info).items():
                    res_file_info += " <a href=""/document_show/?file_id=" + str(
                        key) + " target=""_blank"" rel=""nofollow noopener noreferrer"" title=" + value + ">报告"+str(i)+"</a>"
                    i = i + 1
                approval_list.append(res_file_info)

            elif res.approval_o_file_info:
                res_file_infos = ""
                for key, value in eval(res.approval_o_file_info).items():
                    res_file_infos += " <a href=""/document_show/?file_id=" + str(
                        key) + " target=""_blank"" rel=""nofollow noopener noreferrer"" title=" + value + ">报告"+str(i)+"</a>"
                    i = i + 1
                approval_list.append(res_file_infos)

            else:
                res_file_infoss = ""
                approval_list.append(res_file_infoss)
            approval_list.append(res.approval_time)
            approval_list.append(res.approval_ip)
            approval_list.append(res.approval_o_path_id)
            approval_list.append(res.approval_id)
            approval_list_add_del.append(approval_list)
    return approval_list_add_del
