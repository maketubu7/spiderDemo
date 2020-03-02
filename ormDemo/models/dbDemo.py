# -*- coding: utf-8 -*-
# @Time    : 2020/2/28 21:01
# @Author  : Deng Wenxing
# @Email   : dengwenxingae86@163.com
# @File    : dbDemo.py
# @Software: PyCharm
from peewee import *
from common.libs.PropertiesUtil import Properties
from datetime import date

props = Properties('mysql.properties').properties
props["port"] = int(props["port"])
db = MySQLDatabase(**props)

class Person(Model):
    ##不设置主键的话 会默认加一个字段id 自增的形式为主键
    ##如果主动设置id 这个字段，那么以主动为准
    person_id = IntegerField(primary_key=True)
    name = CharField(max_length=255,null=False)
    birthday = DateField()

    class Meta:
        database = db
        ##不加这个默认以类名的小写为表名
        # tablename = "users"

class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db # this model uses the "people.db" database

def save_data():
    uncle_bob = Person()
    uncle_bob.person_id = 23
    uncle_bob.name = "1"
    uncle_bob.birthday = date(1960, 1, 15)
    res = uncle_bob.save(force_insert=True)
    print(res)
    # grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
    # herb = Person.create(name='Herb', birthday=date(1950, 5, 5))
    # grandma.save()
    # herb.save()

def query_data():
    ##get只会取出一条记录 在取不到数据时会有异常抛出
    try:
        # bob = Person.select().where(Person.name == 'Bob').get()
        # gra = Person.get(Person.name == 'Grandma')
        # print(bob.name)
        # print(gra.name)

        ##这个方法取不到数据不会抛异常，可以取多条数据，按照列表的方法进行操作
        bobs = Person.select().where(Person.name == 'make')
        for bob in bobs:
            print(bob.name,bob.birthday)
        for bob in bobs:
            bob.name = 'make'
            bob.save() ##不存在数据时新增数据，存在时修改数据
        for bob in bobs:
            bob.delete_instance()

    except Exception as e:
        print(e)
        return




if __name__ == "__main__":
    ##执行创建数据库
    # db.create_tables([Person])
    save_data()
    # query_data()