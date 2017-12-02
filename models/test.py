import random

import pymongo

from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb://localhost:27017")

print("连接数据库成功")

db = client["WebTest"]
# 注意下面的这个mongo的名字里面是不能有空格的
# mongodb_name = "web89"

# db = client[mongodb_name]
# print("创建web成功done")

def insert():
    u = {
        "name": "tao",
        "note": "陶建平",
        "随机值": random.randint(0, 3),
    }

    db.user.insert(u)
    print("done")


# def find():
#     '''
#     find函数封装了如何找到所有的相应的data
#     '''
#     query = {
#         'username': '卡卡卡',
#     }
#     user_list = list(db.User.find(query))
#     print("所有的用户", user_list)

# # find()


name_model = "Topic"

cond = {
    "username": "卡卡卡",
}
qqq = {
    "_id": ObjectId("5a228b6cfe3d262a1f494b80"),
}



def find(data_name, query=None):
    '''
    查找数据
    ===
    find 返回一个可迭代对象，使用 list 函数转为数组
    '''
    data = db[data_name].find(query)
    # print('所有用户', user_list)
    print("所有的数据:", data)

find(name_model, qqq)


def find1():
    query = {
        '随机值': 1,
        'name': 'gua'
    }
    us = list(db.user.find(query))
    print('random 1 ', len(us))
    # for u in us:
    #     print(u['name'])
    #
    # 查询 随机值 大于 1 的所有数据
    query = {
        '随机值': {
            '$gt': 1
        },
    }
    print('random > 1', list(db.user.find(query)))
    #
    # $or 查询
    query = {
        '$or': [
            {
                '随机值': 2,
            },
            {
                'name': 'GUA'
            }
        ]
    }
    us = list(db.user.find(query))
    print('or 查询', us)


def update(collection_name, action="$set", **kwargs):
    """
    criteria: 标准,就是要查询的数据的条件
    action: 动作,就是你查到数据之后要干什么
    option: 一些额外的参数
    """
    db[collection_name].update(kwargs, {action: {"username": "lalala"}})
    print("done")


data = []
print(data[0::])
# dict的参数只能是字符串

