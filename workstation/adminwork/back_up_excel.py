from userworkstation.models import FeedBack
from userworkstation.models import UploadFile
from userworkstation.models import Username
from adminworkstation.models import Path
from adminworkstation.models import SysPath
from adminworkstation.models import PartWord
from adminworkstation.models import PathApproval
import xlwt
from io import BytesIO


def back_up_excel(HttpResponse):
    list_FeedBack = FeedBack.objects.all()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=FeedBack.xls'
    if list_FeedBack:
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
        for obj in list_FeedBack:
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