# -*- coding: utf-8 -*-
import json
from fake_useragent import UserAgent

# 声明集合，保存UA
User_Agent_Set = set()

# 因为 fake_useragent库 获取UA的方式是随机的
# 所以，我们扩大获取UA的次数，尽可能的获取到所有的UA，然后将其添加到集合中自动去重
for i in range(100000):
    # 随机获取UA
    ua = UserAgent().random
    # 将获取到的UA添加到集合中
    User_Agent_Set.add(ua)

# 将集合转换为列表
User_Agent_List = list(User_Agent_Set)

# 查看获取到的UA数：经过多次测试，最多能获取到的UA数为250
print(len(User_Agent_List))

# 将UA保存到文件中
with open('ua.json', 'w') as f:
    json.dump(User_Agent_List, f)
