#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Time: 2024/6/26 21:55
@Author: zhengyu
@File: 尝试使用元组来存储message
@Desc zhengyu 2024/6/26 21:55. + cause
"""
class MyClass:
    def __init__(self, value):
        self.value = value

# 创建两个相同值的 MyClass 实例
obj1 = MyClass(10)
obj2 = MyClass(10)

# 创建包含这两个实例的元组
tuple_of_objects = (obj1, obj2)

# 判断元组中第一个和第二个元素是否是同一个实例
if tuple_of_objects[0] is tuple_of_objects[1]:
    print("These are the same instance.")
else:
    print("These are different instances.")

# 修改元组中第一个元素的属性
tuple_of_objects[0].value = 100

# 打印元组中第二个元素的属性，看是否随之改变
print(tuple_of_objects[1].value)  # Output: 10，因为它们不是同一个实例

# 重新设置第二个元素为第一个元素，使其成为同一个实例
tuple_of_objects = (tuple_of_objects[0], tuple_of_objects[0])

# 再次判断它们是否是同一个实例
if tuple_of_objects[0] is tuple_of_objects[1]:
    print("Now these are the same instance.")
else:
    print("Still different instances.")
