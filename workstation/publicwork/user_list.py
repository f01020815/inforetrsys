from userworkstation.models import Username

def user_list():
    user_list = []
    for res in Username.objects.all():
        user_list.append(res.user_name)
    return user_list