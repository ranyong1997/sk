#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/23 9:58 AM
# @Author  : ranyong
# @Site    :
# @File    : StartWork.py
# @Software: PyCharm
import csv
import time
import random
import common.initMooc_ as mooc_init
import common.lookVideo_ as mook_video
import common.workMain_ as mooc_work

# ****************************************** 配置 ******************************************
for key, value in mooc_init.get_user_all().items():
    # 账号1(大号)
    username1 = key  # 账号
    password1 = value  # 密码
    # 账号2(小号)
    username2 = "20175020140"  # 账号
    password2 = "Ranyong_123"  # 密码

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

    # 保存cookies
    def save_cookies():
        ck = {}
        if username1 and password1:
            ck['ck1'] = mooc_init.login(username1, password1)
            if username2 and password2:
                ck['ck2'] = mooc_init.login(username2, password2)
            else:
                print(">>> 未填写账号2信息，仅刷课不答题!")
        else:
            print("请填写账号1 账号以及密码!!!")
            exit(0)
        return ck


    if __name__ == '__main__':
        for err_n in range(10, 0, -1):
            try:
                user_cookies = save_cookies()
                work_exam_type_map = {0: '作业', 1: '测验', 2: '考试'}
                if is_look_video:
                    mook_video.start(user_cookies['ck1'], is_continue_work)
                    print(">>> 刷课程序运行结束")
                    with open('data/success.csv', 'a+', newline='', encoding='gbk') as f:
                        writer = csv.writer(f)
                        writer.writerow([key, value, '已刷'])
                if not user_cookies.get('ck2', None):
                    with open('data/err.csv', 'a+', newline='', encoding='gbk') as f:
                        writer = csv.writer(f)
                        writer.writerow(
                            ['账号', '密码', '状态'])
                        writer.writerow([key, value, '异常'])
                    exit(0)
                print('-' * 60, '\n' + '-' * 23, '初始化课程中！', '-' * 23, '\n' + '-' * 60, '\n')
                # 0.获取小号的所有课程
                username2course = mooc_work.getMyCourse(user_cookies['ck2'])['list']
                print('[小号] ============= 获取所有课程: \n\t~ %s' % '\n\t~ '.join([x['title'] for x in username2course]))
                if is_withdraw_course:
                    # 1.退出小号的所有课程
                    for u2course_item in username2course:
                        work_withdraw_course = mooc_work.run_work_withdraw_course(user_cookies['ck1'],
                                                                                  u2course_item['id'],
                                                                                  u2course_item['stuId'])
                        print('[小号] 退出课程: %s \t结果: %s' % (u2course_item['title'], work_withdraw_course['msg']))
                # 2.获取大号的所有课程
                username1course = mooc_work.getMyCourse(user_cookies['ck1'])['list']
                print('【大号】============= 获取所有课程: \n\t~ %s' % '\n\t~ '.join([x['title'] for x in username1course]))
                # 3.添加大号课程给小号
                for u1course_item in username1course:
                    if u1course_item['id'] in [x['id'] for x in username2course]:
                        print('[小号] 添加课程: %s \t结果: 课程已存在!' % (u1course_item['title']))
                    else:
                        work_add_my_mooc_course = mooc_work.addMyMoocCourse(user_cookies['ck2'],
                                                                            u1course_item['id'])
                        print('[小号] 添加课程: %s \t结果: %s' % (
                            u1course_item['title'], work_add_my_mooc_course.get('msg', 'Fail')))
                # 4.再次查看小号课程
                username2course = mooc_work.getMyCourse(user_cookies['ck2'])['list']
                print('[小号] ============= 获取所有课程: \n\t~ %s' % '\n\t~ '.join([x['title'] for x in username2course]))
                print('\n' + '-' * 65, '\n' + '-' * 20, '初始化课程成功，开始答题！', '-' * 20, '\n' + '-' * 65, '\n')
                # # 5.小号做作业，考试，测验
                work_exam_type = []
                if is_work_exam_type0:
                    work_exam_type.append(0)
                if is_work_exam_type1:
                    work_exam_type.append(1)
                if is_work_exam_type2:
                    work_exam_type.append(2)
                for t in work_exam_type:
                    for u1course in username1course:
                        print('username1course: %s' % username1course)
                        if u1course['title'] in is_continue_work:
                            print('【大号】 跳过课程 \t当前课程 \t【%s】' % u1course['title'])
                            continue
                        # 6.大号开始答题
                        print('【大号】 开始答题 \t当前课程 \t【%s】' % u1course['title'])
                        # todo: run_start_work需要重新抓取接口
                        # mooc_work.run_start_work(user_cookies['ck1'], user_cookies['ck2'], t, u1course['id'],
                        #                          is_work_score)
                print('\n' + '=' * 65, '\n' + '=' * 20, '运行结束 感谢使用',
                      '=' * 20,
                      '\n' + '=' * 65, '\n')
                break
            except Exception as e:
                sleep_int = random.randint(20, 60)
                print(f'程序出现异常，延时 {sleep_int}s 后重试，剩余重试次数: {err_n}，等待重试 {e}')
                time.sleep(sleep_int)
                continue
