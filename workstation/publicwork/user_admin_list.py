from userworkstation.models import Username

def user_admin_list():
    admin_list = []
    for res in Username.objects.filter(user_identity='管理员'):
        admin_list.append(res.user_name)
    return admin_list