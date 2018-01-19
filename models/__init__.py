import json
import time
import random

from utils import log

import pymongo
from pymongo import MongoClient
# 首先要连接mongodb,如果你什么都不写就连接默认的地址
client = MongoClient()


# 如果没有数据插入,你就算执行了下面两句他也不会在robomongo里面显示
# 获取或者创建数据库 如果没有就自己创建一个
db = client["WebTest"]

# 下面这个是获取或者创建一个collection,同样的,如果没有就自己创建一个
# collection = db["haha"]

class Model(object):
    """
    Model 是所有 model 的基类
    Model 是一个 ORM（object relation mapper）
    """
    @classmethod
    def insert(cls, form):
        """
        插入数据
        ===
        使用insert函数插入各种对象
        args:
            form: dict, 代表着对象的各种属性;
            document_name: str, 代表这要创建的collection的名字, 点语法不支持字符串,所以使用[];
        """
        db[cls.__name__].insert(form)

    @classmethod
    def find(cls, query=None):
        '''
        查找数据
        ===
        find 返回一个可迭代对象，使用 list 函数转为数组
        args:
            data_name: str, 就是所要查找的document的名字
            query: dict, 就是要查找的约束条件, 默认是None, Bson竟然也识别的出来
        return:
            返回的是一个包含所有对象的属性的列表
        '''
        # data = list(db[data_name].find(query, {"_id": 0}))
        data = list(db[cls.__name__].find(query))
        return data

    @classmethod
    def _new_from_dict(cls, d):
        """
        """
        # 因为子元素的 __init__ 需要一个 form 参数
        # 所以这个给一个空字典
        m = cls({})
        for k, v in d.items():
            # setattr 是一个特殊的函数
            # 假设 k v 分别是 'name'  'gua'
            # 它相当于 m.name = 'gua'
            setattr(m, k, v)
        return m

    @classmethod
    def new(cls, form, **kwargs):
        """
        """
        m = cls(form)
        for k, v in kwargs.items():
            setattr(m, k, v)
        m.save()
        return m

    @classmethod
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        ===
        args:
            cls
        return:

        """
        models = cls.find()
        # 这里用了列表推导生成一个包含所有 实例 的 list
        # 因为这里是从 存储的数据文件 中加载所有的数据
        # 所以用 _new_from_dict 这个特殊的函数来初始化一个数据
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod
    def find_all(cls, **kwargs):
        """
        根据给定的关键词参数组成的dict,在数据库中寻找相应的数据
        ===
        args
            kwargs: 关键词参数, 给定的查询条件,如author_id=ObjectId(***)
        return
            models: 通过找到的数据重构的一系列实例对象
        """
        data_name = cls.__name__
        data = cls.find(kwargs)
        models = [cls._new_from_dict(m) for m in data]
        return models

    @classmethod
    def find_by(cls, **kwargs):
        """
        根据给定的关键词参数组成的dict,在数据库中寻找相应的数据
        ===
        args
            kwargs: 关键词参数, 给定的查询条件,如author_id=ObjectId(***)
        return
            model: 通过找到的数据重构的一系列实例对象
        """
        data = db[cls.__name__].find_one(kwargs)
        if data is not None:
            model = cls._new_from_dict(data)
            return model
        return None

    @classmethod
    def find_byPage(cls, page=0, sort_by=None, **kwargs):
        """
        根据给定的page和条件找到相应的topic
        ===
        args
            kwargs: 关键词参数, 给定的查询条件,如板块ID
        return
            model: 通过找到的数据重构的一系列实例对象
        """
        if page == 0 or page == 1:
            data = list(db[cls.__name__].find(kwargs).sort([(sort_by, -1)]).limit(7).skip(0))
            if data is not None:
                models = [cls._new_from_dict(m) for m in data]
                return models
        else:
            data = list(db[cls.__name__].find(kwargs).sort([(sort_by, -1)]).limit(7).skip((page-1)*7))
            if data is not None:
                models = [cls._new_from_dict(m) for m in data]
                return models
        return None

    @classmethod
    def get_collection_number(cls, **kwargs):
        """
        根据给定的关键词参数组成的dict,在数据库中寻找相应的数据
        ===
        args
            kwargs: 关键词参数, 给定的查询条件,如author_id=ObjectId(***)
        return
            model: 通过找到的数据重构的一系列实例对象
        """
        number = db[cls.__name__].find(kwargs).count()
        return number

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def json(self):
        """
        返回当前 model 的字典表示
        """
        # copy 会复制一份新数据并返回
        d = self.__dict__.copy()
        return d

    def update(self):
        """
        更新一个现有的数据, 以后可以用update函数提升性能,现在就先用mongodb里面的save函数
        ===
        args
            collection_name: str, 这个是要改的集合的名字
            kwargs: dict, 这个是要更新的那个对象的所有属性
        """
        collection_name = self.__class__.__name__
        attributes = self.__dict__
        db[collection_name].save(attributes)

    def save(self):
        """
        插入一个全新的数据,跟update完全不同,这个实际上用的是insert
        ===
        args: 
            instance
        """
        form = self.__dict__
        # 经历过insert也就是mongodb的插入函数调用之后, 会自动插入一个"_id"数值
        self.insert(form)
        # log("m的属性格式", m.__dict__)
        # 所以要把这个"_id"删除, 不然JSON无法保存
        # m.__dict__.pop("_id")
        # 忽然发现__dict__函数就可以操作他的所有属性

    def to_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.ct))

    @classmethod
    def find_by_sort(cls, con, **kwargs):
        ms = list(db[cls.__name__].find(kwargs).sort(con, pymongo.DESCENDING))
        return ms
        
