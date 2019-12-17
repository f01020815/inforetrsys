import logging
from workstation.publicwork.user_detail import user_detail


def normal(request, action, *args):
    '''

    :param reuqest:用户ip地址
    :param action:操作动作
    :param args: 关键字【0】， pathid【1】
    :return:
    '''

    logger = logging.getLogger('cons')
    logger.info("<用户操作>用户:%s; | 操作:%s; | key_word:%s; | part_id:%s" % (user_detail(request)[1], action, args[0],args[1] ))


def normal_show(request, action, *args):
    logger = logging.getLogger('cons')
    logger.info("<用户操作>用户:%s; | 操作:%s; | key_word:%s; | count:%s" % (user_detail(request)[1], action, args[0], args[1]))
    file = open("LOG/alllog", 'rt')

def custom(request, action, *args):
    '''

    :param reuqest:用户ip地址
    :param action:操作动作
    :param args: 关键字【0】， pathid【1】
    :return:
    '''
    logger = logging.getLogger('custom')
    logger.info("<用户操作>用户:%s; | 操作:%s; | key_word:%s; | part_id:%s" % (user_detail(request)[1], action, args[0],args[1] ))
