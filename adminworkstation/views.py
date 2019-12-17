# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render
from workstation.adminwork.delete_file import delete_file
from workstation.publicwork.upload_file import upload_file
from workstation.adminwork.execl_to_path import execl_to_path
from DBoperation.DBadmin.DBapproval_find_add_del import DBapproval_find_add_del
from DBoperation.DBadmin.DBapproval_find_update import DBapproval_find_update
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,response
from DBoperation.DBadmin.DBapproval_agree_del import DBapproval_agree_del
from DBoperation.DBadmin.DBapproval_agree_ins import DBapproval_agree_ins
from DBoperation.DBadmin.DBapproval_agree_update import DBapproval_agree_update
from DBoperation.DBadmin.DBapproval_reject_del import DBapproval_reject_del
from DBoperation.DBadmin.DBapproval_reject_ins import DBapproval_reject_ins
from DBoperation.DBadmin.DBapproval_reject_update import DBapproval_reject_update
from userworkstation.models import FeedBack, Username
from django.shortcuts import redirect
from workstation.publicwork.user_detail import user_detail
from workstation.publicwork.log_record import normal
from adminworkstation.models import Path
import xlwt
from io import BytesIO
from DBoperation.DBadmin.DBapproval_agree_delfile import DBapproval_agree_delfile
from DBoperation.DBadmin.DBapproval_reject_delfile import DBapproval_reject_delfile
from DBoperation.DBadmin.DBapproval_user_approval import DBapproval_user_approval
import datetime
import time
import calendar
from workstation.publicwork.user_admin_list import user_admin_list
import os
import codecs
# 获取当前时间
localtime = time.strftime('%Y-%m',time.localtime(time.time()))

# 管理员批量上传execl文件
def admingo(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        is_user = request.session.get('user_name', None)
        if is_user in user_admin_list():
            count = 0
            if request.method == 'POST':
                # 获取用户上传的任意格式文件，并记录文件个数
                files = request.FILES.getlist("file", None)

                # 指定文件路径和文件类型，并标注是管理员从execl批量导入数据库
                path = 'TRANSACTION_PATH'
                file_types = ['XLS', 'XLSX']
                source = 'execl'

                # 删除指定目录的指定类型文件
                delete_file(path, file_types)

                # 将指定类型的文件上传至指定目录，并筛取指定类型的文件列表给下个函数使用
                result = upload_file(files, path, file_types)
                if 'all_files' in result:
                    # 读execl表,插入Path表(参数result['specify_files']是从upload_file函数中return回来的)，return回来新插入记录的path_id
                    # count为插入的总条数
                    count = execl_to_path(request, result['all_files'], path, source)
                    # 插入Path表后获取新插入记录的path_id列表，插入索引表(该动作暂时在execl_to_path中判断准许插入Path表后继续插入索引处操作)
                else:
                    pass
                return render(request, 'admingo.html', {'count': count, 'code': result['code']})
            return render(request, 'admingo.html')
        else:
            return render(request, 'login.html', {'page': "admingo"})
    else:
        return render(request, 'login.html', {'page': "admingo"})

# 意见反馈展示
def feedback_show(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        is_user = request.session.get('user_name', None)
        if is_user in user_admin_list():
            result = {}
            feedback_lists = []
            for x in FeedBack.objects.all():
                feedback_list = []
                feedback_list.extend([x.feedback_id])
                feedback_list.extend([x.feedback_words])
                feedback_list.extend([x.feedback_user])
                feedback_list.extend([x.feedback_num])
                feedback_lists.append(feedback_list)
                result['feedback_list'] = feedback_lists
            return render(request, 'feedback_show.html', result)
        return render(request, 'login.html', {'page': "feedback_show"})
    else:
        return render(request, 'login.html', {'page': "feedback_show"})

# 意见反馈一键导出
def export_excel(request):
    city = request.POST.get('city')
    list_obj = FeedBack.objects.all()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=' + city +'.xls'
    if list_obj:
        # 创建工作簿
        ws = xlwt.Workbook(encoding='utf-8')
        # 添加第一页数据表
        w = ws.add_sheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
        # 写入表头
        w.write(0, 0, u'反馈内容')
        w.write(0, 1, u'反馈人员')
        w.write(0, 2, u'联系电话')
        w.write(0, 3, u'主机名称')
        w.write(0, 4, u'用户IP')
        w.write(0, 5, u'MAC地址')
        w.write(0, 6, u'反馈时间')
        # 写入数据
        excel_row = 1
        for obj in list_obj:
            feedback_words = obj.feedback_words
            feedback_user = obj.feedback_user
            feedback_num = obj.feedback_num
            feedback_hostname = obj.feedback_hostname
            feedback_ip = obj.feedback_ip
            feedback_mac = obj.feedback_mac
            feedback_time = obj.feedback_time
            # 写入每一行对应的数据
            w.write(excel_row, 0, feedback_words)
            w.write(excel_row, 1, feedback_user)
            w.write(excel_row, 2, feedback_num)
            w.write(excel_row, 3, feedback_hostname)
            w.write(excel_row, 4, feedback_ip)
            w.write(excel_row, 5, feedback_mac)
            w.write(excel_row, 6, '%s' % feedback_time)
            excel_row += 1
        # 写出到IO
        output = BytesIO()
        ws.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
    return response


# 意见反馈删除
@csrf_exempt
def feedback_del(request):
    if request.is_ajax():
        feedback_id = request.POST.get("feedback_id")
        log = []
        for x in FeedBack.objects.filter(feedback_id=feedback_id):
            log.extend([x.feedback_words])
            log.extend([x.feedback_user])
            log.extend([x.feedback_num])
        FeedBack.objects.filter(feedback_id=feedback_id).delete()
        normal(request, '删除意见', log, 0)
        return redirect("/feedback")


# 审批展示 # add by wangshibin 20190723
def approval(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        is_user = request.session.get('user_name', None)
        if is_user in user_admin_list():
            # 标注管理员页面DBapproval_user_approval
            user = "admin"
            # 搜索审批表中的增加，删除项
            approval_list_add_del = DBapproval_find_add_del(user)
            if len(approval_list_add_del) == 0:
                approval_list_add_del = ''
            # 搜索审批表中的更新项
            approval_list_update = DBapproval_find_update(user)
            if len(approval_list_update) == 0:
                approval_list_update = ''
            return render(request, 'approval.html', {'approval_list_add_del': approval_list_add_del, 'approval_list_update': approval_list_update})
        else:
            return render(request, 'login.html', {'page': "approval"})
    else:
        return render(request, 'login.html', {'page': "approval"})

# 审批同意 # add by wangshibin 20190723
@csrf_exempt
def agree(request):
    if request.is_ajax():
        approval_opt = request.POST.get("opt")
        approval_o_path_id = request.POST.get("path_id_old")
        approval_id = request.POST.get("approval_id")
        log = []
        for x in Path.objects.filter(path_id=approval_o_path_id):
            log.extend([x.path_linetype])
            log.extend([x.path_content])
            log.extend([x.path_tradetype])
            log.extend([x.path_tradepath])
            log.extend([x.path_remark])
        if approval_opt == "删除":
            DBapproval_agree_del(approval_o_path_id, approval_id)
            normal(request, '同意删除', log, approval_o_path_id)
        elif approval_opt == "增加":
            DBapproval_agree_ins(approval_o_path_id, approval_id)
            normal(request, '同意增加', log, approval_o_path_id)
        elif approval_opt == "修改":
            DBapproval_agree_update(approval_o_path_id, approval_id)
            normal(request, '同意修改', log, approval_o_path_id)
    return HttpResponse()


# 审批不同意 # add by wangshibin 20190723
@csrf_exempt
def reject(request):
    if request.is_ajax():
        approval_opt = request.POST.get("opt")
        approval_o_path_id = request.POST.get("path_id_old")
        approval_id = request.POST.get("approval_id")
        # 获取用户信息（判断是管理员admin还是普通用户usr）
        user = request.POST.get("user")
        #获取数据列表，为log提供数据源
        log = []
        for x in Path.objects.filter(path_id=approval_o_path_id):
            log.extend([x.path_linetype])
            log.extend([x.path_content])
            log.extend([x.path_tradetype])
            log.extend([x.path_tradepath])
            log.extend([x.path_remark])

        if approval_opt == "删除":
            DBapproval_reject_del(approval_o_path_id, approval_id)
            if user == "usr":
                normal(request, '撤销删除', log, approval_o_path_id)
            else:
                normal(request, '拒绝删除', log, approval_o_path_id)
        elif approval_opt == "增加":
            DBapproval_reject_ins(approval_o_path_id, approval_id)
            if user == "usr":
                normal(request, '撤销增加', log, approval_o_path_id)
            else:
                normal(request, '拒绝增加', log, approval_o_path_id)
        elif approval_opt == "修改":
            DBapproval_reject_update(approval_o_path_id, approval_id)
            if user == "usr":
                normal(request, '撤销修改', log, approval_o_path_id)
            else:
                normal(request, '拒绝修改', log, approval_o_path_id)
    return HttpResponse()

# 默认获取当日
def log_show(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        is_user = request.session.get('user_name', None)
        if is_user in user_admin_list():
            file = open("LOG/alllog", 'rt')
            file1 = open("LOG/collectlog", 'rt')
            data1 = []
            data2 = []
            for line in file.readlines():
                curline1 = line.strip().split(" | ")
                curline1[0] = curline1[0].replace('<', '')
                curline1[0] = curline1[0].replace('>', '')
                curline1[1] = curline1[1].replace('<', '')
                curline1[1] = curline1[1].replace('>', '')
                curline1[2] = curline1[2].replace('<用户操作>用户:', '')
                curline1[2] = curline1[2].replace(';', '')
                curline1[3] = curline1[3].replace('操作:', '')
                curline1[3] = curline1[3].replace(';', '')
                curline1[4] = curline1[4].replace('key_word:[', '')
                curline1[4] = curline1[4].replace('];', '')
                curline1[5] = curline1[5].replace('part_id:', '')
                data1.append(curline1)
            for line2 in file1.readlines():
                curline2 = line2.strip().split(" | ")
                curline2[0] = curline2[0].replace('<', '').replace('>', '')
                curline2[1] = curline2[1].replace('<', '').replace('>', '')
                curline2[2] = curline2[2].replace('<用户操作>用户:', '').replace(';', '')
                curline2[3] = curline2[3].replace('操作:', '').replace(';', '')
                curline2[4] = curline2[4].replace('key_word:[', '').replace('];', '')
                curline2[5] = curline2[5].replace('part_id:', '')
                data2.append(curline2)
            data = data1 + data2
            return render(request, 'log_show.html', {'log_data': data})
        else:
            return render(request, 'login.html', {'page': "log_show"})
    else:
        return render(request, 'login.html', {'page': "log_show"})


# 按日期获取日志内容
@csrf_exempt
def log_filter(request):
    if request.method == 'POST':
        word_level = request.POST.get('word_level')
        word_action = request.POST.get('word_action')
        word_user = request.POST.get('word_user')
        start_time = request.POST.get('starttime')
        end_time = request.POST.get('endtime')
        try:
            datestart = datetime.datetime.strptime(start_time, '%Y-%m-%d')
            dateend = datetime.datetime.strptime(end_time, '%Y-%m-%d')
            data_list = list()
            while datestart <= dateend:
                data_list.append(datestart.strftime('%Y-%m-%d'))
                datestart += datetime.timedelta(days=1)
        except(Exception):
            data_list = []
            day_now = time.localtime()
            start_time = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)  # 月初肯定是1号
            wday, monthRange = calendar.monthrange(day_now.tm_year,day_now.tm_mon)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
            end_time = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
            datestart = datetime.datetime.strptime(start_time, '%Y-%m-%d')
            dateend = datetime.datetime.strptime(end_time, '%Y-%m-%d')

            while datestart <= dateend:
                data_list.append(datestart.strftime('%Y-%m-%d'))
                datestart += datetime.timedelta(days=1)
    # # 方法一
    # # 获取本地所有文件名称
    # all_filelist = []
    # for path, dirs, file_list in os.walk("LOG"):
    #     for file in file_list:
    #         all_filelist.append(os.path.join(path, file))
    #
    # # 将date_list有对应文件的日期提取出来
    # show_filelists = []
    # for i in data_list:
    #     for s in all_filelist:
    #         if i in s:
    #             show_filelists.append(s)

    # 方法二
    # 将 data_list 加工变为带目录的文件名
    date_filelist_alllog = []
    date_filelist_collectlog = []
    localtime_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    for date in data_list:
        # 如果是当日，则加入/alllog
        if date == localtime_date:
            date_file_alllog = "LOG/alllog"
            date_filelist_alllog.append(date_file_alllog)
            date_file_collectlog = "LOG/collectlog"
            date_filelist_collectlog.append(date_file_collectlog)

        # 如果是本月，则在"LOG/"文件夹中
        elif localtime in date:
            date_file_alllog = "LOG/alllog."+ date
            date_filelist_alllog.append(date_file_alllog)
            date_file_collectlog = "LOG/collectlog." + date
            date_filelist_collectlog.append(date_file_collectlog)

        # 如果是其他月，则在"LOG/年-月/"文件夹中
        else:
            date_file_alllog = "LOG/" + date[0:7] + "/alllog." + date
            date_filelist_alllog.append(date_file_alllog)
            date_file_collectlog = "LOG/" + date[0:7] + "/collectlog." + date
            date_filelist_collectlog.append(date_file_collectlog)


    # 拼接alllog文件
    if (os.path.exists('LOG/' + "tmp_alllog")):
        os.remove('LOG/' + "tmp_alllog")
    with codecs.open('LOG/tmp_alllog',  "a", encoding='gb18030', errors='ignore') as outfile_allllog:
            for file in date_filelist_alllog:
                if os.path.exists(file):
                    with open(file,"r", encoding='gb18030', errors='ignore') as infile_allllog:
                        for line in infile_allllog:
                            outfile_allllog.write(line)
                        outfile_allllog.write('\r\n')
    outfile_allllog.close()

    # 拼接collectlog文件
    if (os.path.exists('LOG/' + "tmp_collectlog")):
        os.remove('LOG/' + "tmp_collectlog")
    with codecs.open('LOG/tmp_collectlog', "a", encoding='gb18030', errors='ignore') as outfile_collect:
        for file in date_filelist_collectlog:
            if os.path.exists(file):
                with open(file, "r", encoding='gb18030', errors='ignore') as infile_collect:
                    for line in infile_collect:
                        outfile_collect.write(line)
                    outfile_collect.write('\r\n')
    outfile_collect.close()

    # 读取文件
    file = open("LOG/tmp_alllog", 'rt', encoding="gb18030", errors='ignore')
    file1 = open("LOG/tmp_collectlog", 'rt', encoding="gb18030", errors='ignore')
    result = ''
    result1 = ''
    result2 = ''
    res = ''
    res1 = ''
    res_time = ''
    data1 = []
    data2 = []
    for index, line in enumerate(file.readlines()):
        # curline = line.strip().split("|")
        # line = line.strip()
        curtime = line.strip('<').split()
        if curtime:
            if curtime[0] in data_list:
                curline = line.strip().split("|")
                if word_action in curline[3]:
                    result = f"{line}"
                    curline1 = result.strip().split("|")
                    if word_level in curline1[1]:
                        result1 = f"{result}"
                        curline2 = result1.strip().split("|")
                        if word_user in curline2[2]:
                            result2 = f"{line}"
                            curline1 = result2.strip().split(" | ")
                            curline1[0] = curline1[0].replace('<', '').replace('>','')
                            curline1[1] = curline1[1].replace('<', '').replace('>', '')
                            curline1[2] = curline1[2].replace('<用户操作>用户:', '').replace(';', '')
                            curline1[3] = curline1[3].replace('操作:', '').replace(';', '')
                            curline1[4] = curline1[4].replace('key_word:[', '').replace('];', '')
                            curline1[5] = curline1[5].replace('part_id:', '')
                            data1.append(curline1)
    for index, line in enumerate(file1.readlines()):
        # curline = line.strip().split("|")
        curtime = line.strip('<').split()
        if curtime:
            if curtime[0] in data_list:
                curline = line.strip().split("|")
                if word_action in curline[3]:
                    result = f"{line}"
                    curline1 = result.strip().split("|")
                    if word_level in curline1[1]:
                        result1 = f"{result}"
                        curline2 = result1.strip().split("|")
                        if word_user in curline2[2]:
                            result2 = f"{line}"
                            curline3 = result2.strip().split(" | ")
                            curline3[0] = curline3[0].replace('<', '').replace('>', '')
                            curline3[1] = curline3[1].replace('<', '').replace('>', '')
                            curline3[2] = curline3[2].replace('<用户操作>用户:', '').replace(';', '')
                            curline3[3] = curline3[3].replace('操作:', '').replace(';', '')
                            curline3[4] = curline3[4].replace('key_word:[', '').replace('];', '')
                            curline3[5] = curline3[5].replace('part_id:', '')
                            data2.append(curline3)
    data = data1 + data2
    file.close()
    file1.close()
    return render(request, 'log_show.html', {'log_data': data})

def maintenance(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        is_user = request.session.get('user_name', None)
        if is_user in user_admin_list():
            return render(request, 'maintenance.html')
        else:
            return render(request, 'login.html', {'page': "maintenance"})
    else:
        return render(request, 'login.html', {'page': "maintenance"})

def user_management(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        is_user = request.session.get('user_name', None)
        if is_user in user_admin_list():
            res = {}
            user_lists = []
            for x in Username.objects.all():
                user_list = []
                user_list.extend([x.user_id])
                user_list.extend([x.user_name])
                user_list.extend([x.user_password])
                user_list.extend([x.user_identity])
                user_list.extend([x.user_email])
                user_list.extend([x.user_phone])
                user_list.extend([x.user_department])

                user_lists.append(user_list)
                res['user_lists'] = user_lists
            return render(request, 'user_management.html', res)
        else:
            return render(request, 'login.html', {'page': "user_management"})
    else:
        return render(request, 'login.html', {'page': "user_management"})

# 用户删除
@csrf_exempt
def user_del(request):
    if request.is_ajax():
        user_id = request.POST.get("user_id")
        log = []
        for x in Username.objects.filter(user_id=user_id):
            log.extend([x.user_name])
            log.extend([x.user_password])
            log.extend([x.user_phone])
            log.extend([x.user_department])
            log.extend([x.user_email])
            log.extend([x.user_identity])
        Username.objects.filter(user_id=user_id).delete()
        normal(request, '用户删除', log, 0)
        return redirect("/user_management")

def user_approval(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        is_user = request.session.get('user_name', None)
        if is_user in user_admin_list():
            user_list = DBapproval_user_approval()
            try:
                len(user_list[0])
            except(Exception):
                user_list = [[]]
            if len(user_list[0]) == 0:
                user_list = ''
            else:
                pass
            return render(request, 'user_approval.html', {'user_undefined': user_list})
        else:
            return render(request, 'login.html', {'page': "user_approval"})
    return render(request, 'login.html', {'page': "user_approval"})

@csrf_exempt
def agree_user(request):
    if request.is_ajax():
        approval_status = request.POST.get("status")
        approval_user = request.POST.get("opt")
        Username.objects.filter(user_name=approval_user).update(user_status=approval_status)
    return HttpResponse()

@csrf_exempt
def reject_user(request):
    if request.is_ajax():
        approval_status = request.POST.get("status")
        approval_user = request.POST.get("opt")
        Username.objects.filter(user_name=approval_user).delete()
    return HttpResponse()
