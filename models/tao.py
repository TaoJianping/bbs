# import pymongo
from pymongo import MongoClient
import random
# 首先要连接mongodb,如果你什么都不写就连接默认的地址
client = MongoClient()


# 如果没有数据插入,你就算执行了下面两句他也不会在robomongo里面显示
# 获取或者创建数据库 如果没有就自己创建一个
db = client["WebTest"]

# 下面这个是获取或者创建一个collection,同样的,如果没有就自己创建一个
# collection = db["haha"]

# print("创建web成功done")
# form = {
#         "name": "tao",
#         "note": "陶建平",
#         "随机值": random.randint(0, 3),
#         }

# document_name = "web"

def insert(form, collection_name):
    """
    使用insert函数插入各种对象
    form: dict, 代表着对象的各种属性;
    document_name: str, 代表这要创建的collection的名字, 点语法不支持字符串,所以使用[];
    """
    db[collection_name].insert(form)


# class TaoModel(object):
#     @classmethod
#     def _new_from_dict(cls, d):
#         # 因为子元素的 __init__ 需要一个 form 参数
#         # 所以这个给一个空字典
#         m = cls({})
#         for k, v in d.items():
#             # setattr 是一个特殊的函数
#             # 假设 k v 分别是 'name'  'gua'
#             # 它相当于 m.name = 'gua'
#             setattr(m, k, v)
#         return m

#     @classmethod
#     def new(cls, form, **kwargs):
#         """
#         """
#         m = cls(form)
#         for k, v in kwargs.items():
#             setattr(m, k, v) 
#         form = m.__dict__

#         m.save()
#         return m

#     @classmethod
#     def all(cls):
#         """
#         all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
#         """
#         path = cls.db_path()
#         models = load(path)
#         # 这里用了列表推导生成一个包含所有 实例 的 list
#         # 因为这里是从 存储的数据文件 中加载所有的数据
#         # 所以用 _new_from_dict 这个特殊的函数来初始化一个数据
#         ms = [cls._new_from_dict(m) for m in models]
#         return ms

#     @classmethod
#     def find_all(cls, **kwargs):
#         ms = []
#         k, v = '', ''
#         for key, value in kwargs.items():
#             k, v = key, value
#         all = cls.all()
#         for m in all:
#             # 也可以用 getattr(m, k) 取值
#             if v == m.__dict__[k]:
#                 ms.append(m)
#         return ms

#     @classmethod
#     def find_by(cls, **kwargs):
#         """
#         用法如下，kwargs 是只有一个元素的 dict
#         u = User.find_by(username='gua')
#         """
#         k, v = '', ''
#         for key, value in kwargs.items():
#             k, v = key, value
#         all = cls.all()
#         for m in all:
#             # 也可以用 getattr(m, k) 取值
#             if v == m.__dict__[k]:
#                 return m
#         return None

#     @classmethod
#     def find(cls, id):
#         return cls.find_by(id=id)

#     @classmethod
#     def delete(cls, id):
#         models = cls.all()
#         index = -1
#         for i, e in enumerate(models):
#             if e.id == id:
#                 index = i
#                 break
#         # 判断是否找到了这个 id 的数据
#         if index == -1:
#             # 没找到
#             pass
#         else:
#             obj = models.pop(index)
#             l = [m.__dict__ for m in models]
#             path = cls.db_path()
#             save(l, path)
#             # 返回被删除的元素
#             return obj

#     def __repr__(self):
#         """
#         __repr__ 是一个魔法方法
#         简单来说, 它的作用是得到类的 字符串表达 形式
#         比如 print(u) 实际上是 print(u.__repr__())
#         """
#         classname = self.__class__.__name__
#         properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
#         s = '\n'.join(properties)
#         return '< {}\n{} \n>\n'.format(classname, s)

#     def json(self):
#         """
#         返回当前 model 的字典表示
#         """
#         # copy 会复制一份新数据并返回
#         d = self.__dict__.copy()
#         return d

#     def save(self):
#         """
#         用 all 方法读取文件中的所有 model 并生成一个 list
#         把 self 添加进去并且保存进文件
#         """
#         # log('debug save')
#         models = self.all()
#         # log('models', models)
#         # 如果没有 id，说明是新添加的元素
#         if self.id is None:
#             # 设置 self.id
#             # 先看看是否是空 list
#             if len(models) == 0:
#                 # 我们让第一个元素的 id 为 1（当然也可以为 0）
#                 self.id = 1
#             else:
#                 m = models[-1]
#                 # log('m', m)
#                 self.id = m.id + 1
#             models.append(self)
#         else:
#             # index = self.find(self.id)
#             index = -1
#             for i, m in enumerate(models):
#                 if m.id == self.id:
#                     index = i
#                     break
#             log('debug', index)
#             models[index] = self
#         l = [m.__dict__ for m in models]
#         path = self.db_path()
#         save(l, path)
