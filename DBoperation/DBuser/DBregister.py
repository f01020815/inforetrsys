from userworkstation.models import Username

def insert_user(*args):
    message = Username()
    num = len(Username.objects)
    name_id = num + 1

    message.user_id = name_id
    message.user_name = args[0]
    message.user_password = args[1]
    message.user_phone = args[2]
    message.user_email = args[3]
    message.user_department = args[4]
    message.user_identity = args[5]
    message.user_status = args[6]

    message.save()
