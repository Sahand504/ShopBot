from models import user_profile


def search_user(user_id):
    user = user_profile.find_user_by_uid(user_id)
    return user


def insert_user(user_id, firstname="", lastname=""):
    user_profile.insert_by_uid(user_id, firstname, lastname)


def update_user(user_id, field, value):
    user_profile.update_by_uid(user_id, field, value)


def get_start_message(effective_user):
    user = search_user(effective_user["id"])
    if user is None:
        insert_user(effective_user["id"], effective_user["first_name"], effective_user["last_name"])
        return "Hello %s and Welcome to ShopBot \n We advice to complete your user profile to search products easily." % str(effective_user["first_name"])
    else:
        return "Hello and welcome back %s" % user["first_name"]



