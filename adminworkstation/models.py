import mongoengine
import datetime

"""
获取接口传值
path表
-----------------------------
path_id	ID-主键
path_linetype	连接类型（联机/批量/MQ联机）
path_content	交易描述(关键业务类型详细描述)
path_tradetype	交易类型（转账，查询，消费）
path_tradepath	交易路由交易路径
path_remark	备注说明
path_update_time	创建时间
path_last_time	最后更新时间
path_hostname	主机名
path_ip	用户IP
path_mac	MAC地址
path_show_state	显示状态	（0不显示，1显示）
path_approval_state	审批状态	（0审核中，1生效）
path_hash	上传excel的hash值
-----------------------------
"""


class Path(mongoengine.Document):
    path_id = mongoengine.IntField(primary_key=True)
    path_linetype = mongoengine.StringField(max_length=30000)
    path_content = mongoengine.StringField(max_length=30000)
    path_tradetype = mongoengine.StringField(max_length=30000)
    path_tradepath = mongoengine.StringField(max_length=30000)
    path_remark = mongoengine.StringField(max_length=30000)
    path_update_time = mongoengine.DateTimeField(default=datetime.datetime.now)
    path_last_time = mongoengine.DateTimeField(default=datetime.datetime.now)
    path_hostname = mongoengine.StringField(max_length=30000)
    path_ip = mongoengine.StringField(max_length=30000)
    path_mac = mongoengine.StringField(max_length=30000)
    path_show_state = mongoengine.IntField(max_length=30000, default=1)
    path_approval_state = mongoengine.IntField(max_length=30000, default=1)
    path_hash = mongoengine.StringField(max_length=100)


"""
获取接口传值
TradePath  交易路由交易路径索引
-----------------------------
tradepath_id   ID-主键
tradepath_name 系统名称
tradepath_list path表ID集合

-----------------------------
"""


class SysPath(mongoengine.Document):
    syspath_id = mongoengine.IntField(primary_key=True)
    syspath_name = mongoengine.StringField(max_length=30000)
    syspath_list = mongoengine.StringField(max_length=30000)


"""
获取接口传值
PartWord   中文分词
-----------------------------
PartWord_id    ID-主键
PartWord_name  分词名词
PartWord_list  path表ID集合
-----------------------------
"""


class PartWord(mongoengine.Document):
    partword_id = mongoengine.IntField(primary_key=True)
    partword_name = mongoengine.StringField(max_length=30000)
    partword_list = mongoengine.StringField(max_length=30000)


"""
PathApproval 审批
-----------------------------
approval_id	ID-主键
approval_opt	操作类型（增加，删除，修改）
approval_o_path_id	所修改的旧的path_id
approval_linetype	连接类型
approval_content	业务描述
approval_tradetype	交易类型
approval_tradepath	交易路由
approval_remark	备注说明
approval_time	提交时间（用户操作时间）
approval_hostname	主机名
approval_ip	用户IP
approval_mac	MAC地址
approval_file_info	需要审批的文档ID 文档名称
approval_o_file_info	已有文档ID  文档名称
approval_path_id_b	关联ID(用于新增时记录更新前path_id)
-----------------------------
"""


class PathApproval(mongoengine.Document):
    approval_id = mongoengine.IntField(primary_key=True)
    approval_opt = mongoengine.StringField(max_length=30000)
    approval_o_path_id = mongoengine.StringField(max_length=30000)
    approval_linetype = mongoengine.StringField(max_length=30000)
    approval_content = mongoengine.StringField(max_length=30000)
    approval_tradetype = mongoengine.StringField(max_length=30000)
    approval_tradepath = mongoengine.StringField(max_length=30000)
    approval_remark = mongoengine.StringField(max_length=30000)
    approval_time = mongoengine.DateTimeField(default=datetime.datetime.now)
    approval_hostname = mongoengine.StringField(max_length=30000)
    approval_ip = mongoengine.StringField(max_length=30000)
    approval_mac = mongoengine.StringField(max_length=30000)
    approval_n_file_info = mongoengine.StringField(max_length=30000)
    approval_o_file_info = mongoengine.StringField(max_length=30000)
    approval_path_id_b = mongoengine.StringField(max_length=30000)
