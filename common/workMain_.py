#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/4/23 9:57 AM
# @Author  : ranyong
# @Site    :
# @File    : workMain.py
# @Software: PyCharm
import csv
import json
import logging
import random
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = 'https://www.icve.com.cn'
# 获取我加入的所有课程
# GET_MY_COURSE_URL = BASE_URL + '/portal/Course/getMyCourse'
GET_MY_COURSE_URL = BASE_URL + '/studycenter/MyCourse/studingCourse'

# 获取本课程 作业/测验/考试 ID api
# https://www.icve.com.cn/study/Stat/getTable
GET_WORK_EXAM_LIST_URL = BASE_URL + '/study/Stat/getTable'

# 做作业 api
# https://www.icve.com.cn/study/directory/directory
WORK_EXAM_PREVIEW_URL = 'https://www.icve.com.cn/study/directory/view'

# 提交作业/测验 api
WORK_EXAM_SAVE_URL = f'{BASE_URL}/study/workExam/workExamSave'

# 提交考试 api
# https://www.icve.com.cn/study/directory/subPaper
ONLINE_EXAM_SAVE_URL = f'{BASE_URL}/study/directory/subPaper'

# 查看答案
# https://www.icve.com.cn/study/directory/view
WORK_EXAM_HISTORY_URL = BASE_URL + '/study/directory/view'

# 查看作答列表
WORK_EXAM_DETAIL_URL = BASE_URL + '/study/directory/view'

# 填题目
ONLINE_HOMEWORK_ANSWER = BASE_URL + '/study/workExam/onlineHomeworkAnswer'

# 填题目(填空题)
ONLINE_HOMEWORK_CHECK_SPACE = BASE_URL + '/study/workExam/onlineHomeworkCheckSpace'

# 退出课程
COURSE_WITHDRAW_COURSE = BASE_URL + '/portal/Course/withdrawCourse'

# 获取该课程所有开课信息(一般最新的开课可以加入)
GET_ALL_COURSE_CLASS_URL = BASE_URL + '/portal/Course/getAllCourseClass'

# 用 courseOpenId 去添加课程
# ADD_MY_MOOC_COURSE = BASE_URL + '/study/Learn/addMyMoocCourse'
ADD_MY_MOOC_COURSE = BASE_URL + '/Study/Directory/isCanLearn'
# https://www.icve.com.cn/Study/Directory/isCanLearn?courseId=vzbfafmra6xjnciyxpscq

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}


# cookies = None

# 获取课程列表
def getMyCourse(cookies):
    # isFinished 只获取没有结束的课程
    # https://www.icve.com.cn/studycenter/PersonalInfo/getUserInfo
    # todo:需要userid进行动态渲染
    params = {
        'userid': "yoiagms4fkxowyp0kvwg",
    }
    get = requests.post(url=GET_MY_COURSE_URL, params=params, cookies=cookies, headers=HEADERS)
    return get.json()
    # {'code': 1, 'list': [{'id': 'vzbfafmra6xjnciyxpscq', 'schedule': '0.00', 'datecreated': '2021/12/12 10:07:35',
    # 'title': '国际商务谈判',
    # 'cover': 'https://file.icve.com.cn/file_doc_public/233/39/3A609D2B44686F240FE8E81627065530.jpg?x-oss-process=image/resize,m_fixed,w_198,h_112,limit_0',
    # 'studyhours': '52.0', 'state': '3'}], 'userid': 'yoiagms4fkxowyp0kvwg', 'pagination': {'totalCount': 1, 'pageSize': 12, 'pageIndex': 1}}


# 获获取作业、随堂测验、讨论 没问题✔
def getWorkExamList(cookies, courseid, work_exam_type):
    # todo:因为随堂测试只能查询一页 所以page需要更改才能兼顾其他
    params = {
        'id': work_exam_type,  # 1是作业，2是随堂测试，3是讨论，4是讨论
        'courseId': courseid,
        'serchName': '',
        'page': 1,
    }

    get = requests.post(url=GET_WORK_EXAM_LIST_URL, data=params, cookies=cookies, headers=HEADERS)
    return get.json()  # 获取接口成功返沪True


# 做作业、查看答案
def workExamPreview(cookies, work_exam_id):
    # todo:课程id需要动态获取
    params = {
        'cellId': work_exam_id,
        'courseId': "vzbfafmra6xjnciyxpscq",
        'enterType': 'study'
    }
    post = requests.post(url=WORK_EXAM_PREVIEW_URL, data=params, cookies=cookies, headers=HEADERS)
    print(post.json())
    return post.json()


# 提交作业
def workExamSave(cookies, work_exam_preview, work_exam_type):
    params = {
        'studentWorksId': work_exam_preview['Id']  # 每次一随堂测验id
    }
    if work_exam_type == 2:
        post = requests.post(url=ONLINE_EXAM_SAVE_URL, data=params, cookies=cookies, headers=HEADERS)
    else:
        post = requests.post(url=WORK_EXAM_SAVE_URL, data=params, cookies=cookies, headers=HEADERS)
    return post.json()


def onlineHomeworkAnswer(cookies, question_id, answer, question_type, unique_id):  # 6 填答题卡
    '''
    填答题卡
    :param question_id: 题目ID
    :param answer: 答案
    :param question_type: 1单选 2多选 3判断
    :param unique_id: 每次点做作业都会出现一个id，目前发现不提交作业就不会变
    :return:
    '''
    params = {
        'questionId': question_id,
        'answer': answer,
        'questionType': question_type,
        'uniqueId': unique_id
    }
    post = requests.post(url=ONLINE_HOMEWORK_ANSWER, data=params, cookies=cookies, headers=HEADERS)
    return post.json()


def onlineHomeworkCheckSpace(cookies, question_id, answer, question_type, unique_id):  # 6 填答题卡
    '''
    填答题卡(填空题的特殊处理)
    :param question_id: 题目ID
    :param answer: 答案
    :param question_type: 1单选 2多选 3判断 5填空
    :param unique_id: 每次点做作业都会出现一个id，目前发现不提交作业就不会变
    :return:
    '''
    params = {
        'questionId': question_id,
        'answer': "",
        'answerJson': str([{"Content": answer}]),
        'questionType': question_type,
        'uniqueId': unique_id
    }
    post = requests.post(url=ONLINE_HOMEWORK_CHECK_SPACE, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


def workExamHistory(cookies, work_exam_id, student_work_id):  # 7 获取答案
    params = {
        'cellId': work_exam_id,  # jxggavsukypazpirbudefq
        'courseId': student_work_id,  # vzbfafmra6xjnciyxpscq
        'enterType': "study"  # study
    }
    post = requests.post(url=WORK_EXAM_HISTORY_URL, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


def withdrawCourse(cookies, course_open_id, user_id):  # 8 退出课程
    params = {
        'courseOpenId': course_open_id,
        'userId': user_id
    }
    post = requests.post(url=COURSE_WITHDRAW_COURSE, params=params, cookies=cookies, headers=HEADERS)
    return post.json()


# 添加课程
def addMyMoocCourse(cookies, course_open_id):  # 3 添加到我的课程
    params = {
        'courseOpenId': course_open_id,
        'courseId': 'vzbfafmra6xjnciyxpscq'
    }
    # https://www.icve.com.cn/Study/Directory/isCanLearn?courseId=vzbfafmra6xjnciyxpscq
    get = requests.post(url=ADD_MY_MOOC_COURSE, params=params, cookies=cookies, headers=HEADERS)
    return get.json()  # 添加课程成功返回


def csvUtil(file_name, rows, *headers):  # 写 csv 文件
    # 题目id，作业类型，答案id
    headers = ['questionId', 'questionType', 'Answer']

    with open(file_name + '.csv', 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)


# def csv_to_dict(filename):
#     try:
#         with open(filename, 'r') as read_obj:
#             dict_reader = DictReader(read_obj)
#             list_of_dict = list(dict_reader)
#             result = json.dumps(list_of_dict, indent=2)
#         return result
#     except IOError as err:
#         print("I/O error({0})".format(err))


# def csvUtil(file_name, rows, *headers):  # 写 csv 文件
#     # 课程名， 第几次开课，课程id，作业名，作业id，答案id
#     headers = ['courseName', 'courseOpenName', 'courseOpenId', 'Title', 'workExamId', 'stuWorkExamId']
#
#     with open(file_name + '.csv', 'w', newline='')as f:
#         f_csv = csv.writer(f)
#         f_csv.writerow(headers)
#         f_csv.writerows(rows)

def run_work_withdraw_course(cookies, course_open_id, stu_id):
    return withdrawCourse(cookies, course_open_id, stu_id)


work_exam_type_map = {1: '作业', 2: '随堂测试', 3: '讨论', 4: '考试'}
question_type_type_map = {
    1: '单选题',
    2: '多选题',
    3: '判断题',
    5: '填空题',
    6: '问答题',
    7: '匹配题',
    8: '阅读理解题',
    10: '文件作答题'
}


# 刷随堂测试主逻辑
def run_start_work(ck1, ck2, work_exam_type, course_open_id, is_work_score):
    exam_list = getWorkExamList(ck1, course_open_id, work_exam_type)
    print("查询随堂测试分数： {}".format(exam_list['list']))
    for exam_item in exam_list['list']:
        if exam_item['scorePercentage'] >= is_work_score:
            print('\t1. 当前{%s}: \t分数:%s \t大于预设分数: %s \t不答题 \t【%s】' % (
                work_exam_type_map[work_exam_type], exam_item['scorePercentage'], is_work_score, exam_item['Title']))
            continue
        print('\t1. 当前{%s}:【%s】' % (work_exam_type_map[work_exam_type], exam_item['Title']))
        # 利用小号获取答案
        work_exam_answer_map = run_get_answer(ck2, work_exam_type, course_open_id, exam_item['Id'])
        print("代码运行到这------------1")
        print("work_exam_answer_map--->> {}".format(work_exam_answer_map))
        # work_exam_preview = workExamPreview(ck1, exam_item['Id'])
        # print("代码运行到这------------2")
        # print("work_exam_preview--->> {}".format(work_exam_preview))
        # work_exam_questions = json.loads(work_exam_preview['workExamData'])['questions']
        # answer_count = 0
        # # 循环题目
        # for i in work_exam_questions:
        #     # 查找答案
        #     answer_map = work_exam_answer_map.get(i['questionId'], None)
        #     if answer_map:
        #         if not answer_map['Answer']:
        #             print('\t\t\t3. 作答中... 结果: 找到答案，但答案为空！ \t类型 %s \t题目: %s' % (
        #                 question_type_type_map.get(answer_map['questionType'], '未知'), i['TitleText']))
        #             continue
        #         # TODO: 填空题的特殊处理 (大学生创业基础 黄河水利职业技术学院 所属专业: 公共基础课)
        #         if answer_map['questionType'] == 5:
        #             if len(i['answerList']) > 1:
        #                 print('\t\t\t3. 作答中... 结果: 多个填空，暂不支持，输出答案请注意提取！ \t类型 %s \t题目: %s \t答案: %s' % (
        #                     question_type_type_map.get(answer_map['questionType'], '未知'), i['TitleText'],
        #                     answer_map['Answer']))
        #                 continue
        #             answer_res = onlineHomeworkCheckSpace(ck1, i['questionId'], answer_map['Answer'],
        #                                                   answer_map['questionType'], work_exam_preview['uniqueId'])
        #         # TODO: 匹配题的特殊处理 暂时没有处理（毛泽东思想和中国特色社会主义 课程负责人：张小兰 开课名称：第八次开课 作业：第一章作业
        #         elif answer_map['questionType'] == 7:
        #             print('\t\t\t3. 作答中... 结果: 匹配题暂不支持，输出答案请注意提取！ \t类型 %s \t题目: %s \t答案: %s' % (
        #                 question_type_type_map.get(answer_map['questionType'], '未知'), i['TitleText'],
        #                 answer_map['Answer']))
        #             continue
        #         # TODO: 阅读理解题的特殊处理 暂时没有处理（毛泽东思想和中国特色社会主义 课程负责人：张小兰 开课名称：第八次开课 作业：第一章作业
        #         elif answer_map['questionType'] == 8:
        #             print('\t\t\t3. 作答中... 结果: 阅读理解题暂不支持，输出答案请注意提取！ \t类型 %s \t题目: %s \t答案: %s' % (
        #                 question_type_type_map.get(answer_map['questionType'], '未知'), i['TitleText'],
        #                 answer_map['Answer']))
        #             continue
        #         else:
        #             answer_res = onlineHomeworkAnswer(ck1, i['questionId'], answer_map['Answer'],
        #                                               answer_map['questionType'], work_exam_preview['uniqueId'])
        #         if answer_res['code'] == 1:
        #             answer_count += 1
        #         if answer_map['questionType'] == 1:
        #             answer_map['Answer'] = chr(97 + int(answer_map['Answer'].replace(",", ""))).upper()
        #         if answer_map['questionType'] == 2:
        #             answer_map['Answer'] = ', '.join(
        #                 [chr(97 + int(x)).upper() for x in answer_map['Answer'].split(",") if x is not ''])
        #         if answer_map['questionType'] == 3:
        #             answer_map['Answer'] = '正确' if answer_map['Answer'] == '1' else '错误'
        #         print('\t\t\t3. 作答中... 结果: %s \t类型: %s \t答案: %s \t题目: %s' % (
        #             answer_res.get('allDo', answer_res.get('msg', answer_res['code'])),
        #             question_type_type_map[answer_map['questionType']],
        #             answer_map['Answer'], i['TitleText']))
        #     else:
        #         print('\t\t\t3. 作答中... 结果: 未找到答案！ \t类型 %s \t题目: %s' % (
        #             question_type_type_map[i['questionType']], i['TitleText']))
        # if len(work_exam_questions) == answer_count:
        #     work_exam_save_res = workExamSave(ck1, work_exam_preview['uniqueId'], exam_item['Id'], work_exam_type)
        #     print('\t\t\t\t4. ^v^ 提交作业... 【%s】\t 状态: %s' % (exam_item['Title'], work_exam_save_res['msg']))
        # else:
        #     print('\t\t\t\t4. ~_~ 提交作业... 【%s】\t 状态: 未提交！请前往网页手动提交！注意作答时长！' % (exam_item['Title']))


# 利用小号保存答案
def run_get_answer(cookies, work_exam_type, course_open_id, work_exam_id):
    work_exam_answer_map = {}
    work_exam_list = getWorkExamList(cookies, course_open_id, work_exam_type)
    for work_exam in [i for i in work_exam_list['list'] if i['Id'] == work_exam_id]:
        # 如果状态为空，则表示还未答题;
        if work_exam['Status'] == '':
            # 通过作业ID去交作业(必须先点做作业)
            work_exam_preview = workExamPreview(cookies, work_exam['Cellid'])
            work_exam_save_res = workExamSave(cookies, work_exam_preview['works'], work_exam_type)
            print(work_exam_save_res['msg'])
        else:
            print('当前作业已存在作答记录!')
        # 作业提交成功后，获取我做的所有作业记录，取第一条里面有答案ID
        work_exam_detail = workExamPreview(cookies, work_exam['Cellid'])
        if not work_exam_detail['data']:
            continue
        work_exam_history = work_exam_detail['data']['paper']['PaperQuestions']
        print("work_exam_history--->> {}".format(work_exam_history))
        # for i in json.loads(work_exam_history['workExamData'])['questions']:
        #     work_exam_answer_map[i['questionId']] = {
        #         'questionType': i['questionType'],
        #         'Answer': i['Answer'],
        #     }
        # print('\t\t2. 生成题库中...\t当前{%s}: 【%s】 \t%s' % (work_exam_type_map[work_exam_type], work_exam['Title'], msg))
    return work_exam_answer_map
