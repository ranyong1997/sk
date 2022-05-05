#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/23 9:58 AM
# @Author  : ranyong
# @Site    : 
# @File    : StartWork.py
# @Software: PyCharm
import csv
import common.initMooc as mooc_init

# ****************************************** 配置 ******************************************
for key, value in mooc_init.get_user_all().items():
    # 账号1(大号)
    username1 = key  # 账号
    password1 = value  # 密码
    # 账号2(小号)
    username2 = "cqdxxy1"  # 账号
    password2 = "cqdxxy@123"  # 密码
    # 账号1(大号)刷课
    is_look_video = True
    # 小号退出所有课程
    is_withdraw_course = False
    # 做作业
    is_work_exam_type0 = True
    # 做测验
    is_work_exam_type1 = True
    # 考试
    is_work_exam_type2 = True
    # 大于90分的不进行再次作答
    is_work_score = 90
    # 需要跳过的课程，填写方式例： ['大学语文', '高等数学']
    is_continue_work = ['注射成型技术', '鞋服陈列设计']
# ****************************************** 结束 ******************************************

    if __name__ == '__main__':
        mooc_init.run(
            username1=username1,
            password1=password1,
            username2=username2,
            password2=password2,
            is_look_video=is_look_video,
            is_withdraw_course=is_withdraw_course,
            is_work_exam_type0=is_work_exam_type0,
            is_work_exam_type1=is_work_exam_type1,
            is_work_exam_type2=is_work_exam_type2,
            is_work_score=is_work_score,
            is_continue_work=is_continue_work,
        )
        with open('data/success.csv', 'a+', newline='', encoding='gbk') as f:
            writer = csv.writer(f)
            writer.writerow([key, value, '已刷'])