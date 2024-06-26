"""
appdirs 库主要用于在不同操作系统上提供应用程序目录的标准路径，
包括用户数据目录、用户配置目录、用户缓存目录和用户状态目录等。以下是 appdirs 库的一些常见功能和用法：

"""
import os
import appdirs
import pathlib
import json

AppDirs = appdirs.AppDirs(appname="Wise-Whisper", appauthor="zzy-yzy")
print(AppDirs.user_data_dir) # 获取用户数据目录 用户数据目录用于存储用户数据文件。这些文件通常是用户创建或需要长期保留的数据。

print(pathlib.Path(AppDirs.user_state_dir))
# 2. 获取用户配置目录
print(AppDirs.user_config_dir)

print(AppDirs.user_cache_dir)
print(AppDirs.site_data_dir)

if not os.path.exists(pathlib.Path(AppDirs.user_state_dir)):
    os.makedirs(pathlib.Path(AppDirs.user_state_dir))

# 检查文件是否存在，如果不存在则创建并写入初始内容

with open(pathlib.Path(AppDirs.user_state_dir) / "test.dat", 'w') as f:
    f.write("")
    # print(f"Created {config_file_path}")
# print(dat)

