import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["shop_bot"]
my_col = my_db["profile"]


def find_user_by_uid(user_id):
    user_profile = my_col.find_one({"user_id": user_id})
    return user_profile


def insert_by_uid(user_id, firstname, lastname):
    my_dec = {"user_id": user_id, "first_name": firstname, "last_name": lastname}
    x = my_col.insert_one(my_dec)


def update_by_uid(user_id, field, value):
    query = {"user_id": user_id}
    update_set = {"$set": {field: value}}
    x = my_col.update(query, update_set)


def push_by_uid(user_id, field, value):
    query = {"user_id": user_id}
    update_set = {"$push": {field: value}}
    x = my_col.update(query, update_set, upsert=True)


def pull_by_uid(user_id, field, value):
    query = {"user_id": user_id}
    update_set = {"$pull": {field: value}}
    x = my_col.update(query, update_set, upsert=True)
