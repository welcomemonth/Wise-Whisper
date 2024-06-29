#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/26 22:00
@Author: zhengyu
@File: 自定义类对比方法
@Desc zhengyu 2024/6/26 22:00. + cause
"""


class MyClass:
    def __init__(self, id: str, value: int):
        self.id = id
        self.value = value
    def __eq__(self, other):
        """ 定义相等性判断方式 """
        if isinstance(other, MyClass):
            return self.id == other.id
        return NotImplemented

    def __hash__(self):
        """ 定义哈希值计算方式 """
        return hash(self.id)


# 创建两个不同的 MyClass 实例
obj1 = MyClass("qdasdasd", 100)
obj2 = MyClass("10", 200)
obj3 = MyClass("10", 300)

# 判断两个实例是否相等
print(obj1 == obj2)  # Output: True，根据 __eq__ 方法定义，value 相同则判断为相等
print(obj1 == obj3)  # Output: False，value 不同则判断为不相等
print(obj2 == obj3)  # 通过id判断，相同

tuple_ = (obj1, obj2, obj3)
print(tuple_)

for i in tuple_:
    print(i)

unique_objs = {obj1, obj2, obj3}  # 通过集合将自定义相同的实例剔除
set_tuple_ = tuple(unique_objs)
for i in set_tuple_:
    print(i.value)
    i.value += 1000

for i in set_tuple_:
    print(i.value)

#
# # 使用字典来测试自定义哈希方法
# my_dict = {obj1: 'Object 1', obj2: 'Object 2', obj3: 'Object 3'}
#
# # 查看字典中的值
# print(my_dict[obj1])  # Output: Object 1，因为 obj1 和 obj2 被视为相同的键
#
# # 重新定义 obj2 的值，使其不同于 obj1
# obj2.value = 100
#
# # 现在再次查看字典中的值
# print(my_dict.get(obj1))  # Output: None，因为 obj1 和 obj2 现在被视为不同的键
# print(my_dict.get(obj2))  # Output: Object 2
#
