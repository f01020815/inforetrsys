import mongoengine
import datetime

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


class FeedBack(mongoengine.Document):
    feedback_id = mongoengine.IntField(primary_key=True)
    feedback_words = mongoengine.StringField(max_length=3000)
    feedback_user = mongoengine.StringField(max_length=3000)
    feedback_num = mongoengine.StringField(max_length=3000)
    feedback_hostname = mongoengine.StringField(max_length=3000)
    feedback_ip = mongoengine.StringField(max_length=3000)
    feedback_mac = mongoengine.StringField(max_length=3000)
    feedback_time = mongoengine.DateTimeField(default=datetime.datetime.now)


"""
UploadFile	上传高等级事件
-----------------------------
file_id	ID-主键
file_path_id	path表的path_id
file_path	文档路径
file_name	文档名称
file_load_time	上传时间
file_hostname	主机名称
file_ip	用户IP
file_mac	MAC地址
file_show_state	显示状态	（0不显示，1显示）	
file_approval_state	审批状态	（0审核中，1生效）	

-----------------------------
"""


class UploadFile(mongoengine.Document):
    file_id = mongoengine.IntField(max_length=3000)
    file_path_id = mongoengine.StringField(max_length=3000)
    file_path = mongoengine.StringField(max_length=3000)
    file_name = mongoengine.StringField(max_length=3000)
    file_load_time = mongoengine.DateTimeField(default=datetime.datetime.now)
    file_hostname = mongoengine.StringField(max_length=3000)
    file_ip = mongoengine.StringField(max_length=3000)
    file_mac = mongoengine.StringField(max_length=3000)
    file_show_state = mongoengine.IntField(max_length=30000, default=1)


class Username(mongoengine.Document):
    user_id = mongoengine.IntField(max_length=2000)
    user_name = mongoengine.StringField(max_length=3000)
    user_password = mongoengine.StringField(max_length=3000)
    user_identity = mongoengine.StringField(max_length=3000)
    user_email = mongoengine.StringField(max_length=3000)
    user_phone = mongoengine.StringField(max_length=3000)
    user_department = mongoengine.StringField(max_length=3000)
    user_status = mongoengine.IntField(max_length=1000)
    '''
    user_status参数   0/1 ：0表示未通过 1表示通过
    '''