from userworkstation.models import FeedBack


def feedbackwork(feedback_detail):
    """
    FeedBack	意见反馈
    -----------------------------
    feedback_id	primary_key
    feedback_words	反馈内容
    feedback_user	反馈人员
    feedback_num	联系电话
    feedback_hostname	主机名称
    feedback_ip 	用户IP
    feedback_mac	MAC地址
    feedback_time	反馈时间
    -----------------------------
    """
    message = FeedBack()
    # 获取主键ID的总数，加1后为自增长的ID值
    num = len(FeedBack.objects)
    message.feedback_id = num+1
    # 存储数据words, user, num, hostname, ip, mac
    message.feedback_words = feedback_detail[0]
    message.feedback_user = feedback_detail[1]
    message.feedback_num = feedback_detail[2]
    message.feedback_hostname = feedback_detail[3]
    message.feedback_ip = feedback_detail[4]
    message.feedback_mac = feedback_detail[5]
    # 保存
    message.save()


