from userworkstation.models import Username


def DBapproval_user_approval():
    '''查询所有未审批的用户'''
    approval_undefined = []
    for res in Username.objects.filter(user_status=0):
        approval_list = []
        approval_list.append(res.user_name)
        approval_list.append(res.user_password)
        approval_list.append(res.user_email)
        approval_list.append(res.user_phone)
        approval_list.append(res.user_department)
        approval_undefined.append(approval_list)
    return approval_undefined


