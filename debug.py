import time
import csv
import requests
import json
import ddddocr
from common import UA as UA_tools

ocr = ddddocr.DdddOcr()

headers = {
    'User-Agent': UA_tools.getRandomUA()  # 这里就调用了自己的工具库的方法来随机获取UA
}


def ddocr(file):
    try:
        with open(file, 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        return res
    except:
        print("获取验证码失败，请继续！")


def get_user_all():
    """读取csv至字典"""
    csvFile = open("data/1.csv", "r", encoding='gbk')
    reader = csv.reader(csvFile)
    # 建立空字典
    result = {}
    for item in reader:
        # 忽略第一行
        if reader.line_num == 1:
            continue
        result[item[0]] = item[1]
    csvFile.close()
    return result


# 0.登录，拿到cookie------>https://mooc.icve.com.cn/portal/LoginMooc/loginSystem
def login(key, value):
    '''登录'''
    # 验证码https://mooc.icve.com.cn/portal/LoginMooc/getVerifyCode?ts=1608968080542
    codeUrl = "https://mooc.icve.com.cn/portal/LoginMooc/getVerifyCode?ts={}".format(
        int(round(time.time() * 2000)))
    loginUrl = "https://mooc.icve.com.cn/portal/LoginMooc/loginSystem"
    codeResult = requests.post(url=codeUrl, headers=headers)
    with open("moocCode.jpg", "wb", ) as f:
        f.write(codeResult.content)
    code_cookies = codeResult.cookies  # 获取验证码cookies
    r = ddocr('moocCode.jpg')  # 识别验证码
    print("---------->正在登录{}账号".format(key))
    result = requests.post(url=loginUrl, data={'username': key, 'password': value, 'verifyCode': r},
                           headers=headers, cookies=code_cookies)
    if result.status_code == 200:
        print("登录成功！")
        return result.cookies
    else:
        print("登录失败！")
        return None


# 1.获取所有课程，拿到id-------->https://mooc.icve.com.cn/portal/course/getCourseOpenList
def getCourseOpenList(cookies):
    '''
    获取所有课程
    :param cookies: cookies
    :return: {id: "tmhmacetzyzbiypj2kpxsg", text: "国际商务谈判_第三次开课"}
    '''
    url = "https://mooc.icve.com.cn/portal/course/getCourseOpenList"
    result = json.loads(requests.post(url=url, headers=headers, cookies=cookies).text)
    return result['list']


# 2.得到一级目录-------->https://mooc.icve.com.cn/study/learn/getProcessList?courseOpenId=wylwaxasdyjptaswj67x6g
def getProcessList(cookies, courseId):
    '''
    得到一级目录
    :param cookies: cookies
    :param courseId: gtjkawksy5jf7raso8gdq
    :return: [
    0: {id: "cpzzacmtvphprdd0jmsha", name: "导论", sortOrder: 1, percent: 100, ModuleType: 1, ResId: "",…}
    1: {id: "cpzzacmtq7hlnfrjeftdsg", name: "一、谈——基础理论篇", sortOrder: 2, percent: 100, ModuleType: 1,…}
    2: {id: "cpzzacmtlaho2hbnjkarpw", name: "项目介绍", sortOrder: 3, percent: 100, ModuleType: 1, ResId: "",…}
    3: {id: "dpzzacmt64batiltipb3xa", name: "二、商——项目实践篇", sortOrder: 4, percent: 100, ModuleType: 1,…}
    4: {id: "dpzzacmtc5jm1exlf7c5w", name: "三、论——情境创设篇", sortOrder: 5, percent: 100, ModuleType: 1, ResId: "",…}
    5: {id: "dpzzacmtryph6croy2ynfq", name: "四、道——素质拓展篇", sortOrder: 6, percent: 100, ModuleType: 1,…}
    6: {id: "2sxdacmtlpnle8pf53qjxa", name: "期末测试", sortOrder: 7, percent: 0, ModuleType: 2,…}
    ]
    '''
    url = "https://mooc.icve.com.cn/study/learn/getProcessList"
    result = json.loads(requests.post(url=url, data={'courseOpenId': courseId}, headers=headers, cookies=cookies).text)
    return result['proces']['moduleList']


# 3.得到二级目录-------->https://mooc.icve.com.cn/study/learn/getTopicByModuleId?courseOpenId=wylwaxasdyjptaswj67x6g&moduleId=q4twaxasc7nbpxt8pmkjdw
def getTopicByModuleId(cookies, courseId, moduleId):
    '''
    得到二级目录
    :param cookies: cookies
    :param courseId: courseOpenId
    :param moduleId: moduleId
    :return: [
    0: {id: "cpzzacmtvphprdd0jmsha", name: "导论", sortOrder: 1, percent: 100, ModuleType: 1, ResId: "",…}
    ModuleType: 1
    ResId: ""
    id: "cpzzacmtvphprdd0jmsha"
    isUnlock: true
    name: "导论"
    percent: 100
    sortOrder: 1]
    '''
    url = "https://mooc.icve.com.cn/study/learn/getTopicByModuleId"
    data = {
        'courseOpenId': courseId,
        'moduleId': moduleId
    }
    result = json.loads(requests.post(url=url, data=data, headers=headers, cookies=cookies).text)
    return result['topicList']


# 4.获得三级目录（详细信息）--------->https://mooc.icve.com.cn/study/learn/getCellByTopicId?courseOpenId=wylwaxasdyjptaswj67x6g&topicId=qotwaxasyjbjd0mnjgxz1w
def getCellByTopicId(cookies, courseId, topicId):
    '''
    获得三级目录（详细信息）
    :param cookies: cookies
    :param courseId: courseOpenId
    :param topicId: topicId
    :return: [
    0: {id: "cpzzacmtvphprdd0jmsha", name: "导论", sortOrder: 1, percent: 100, ModuleType: 1, ResId: "",…}
    ModuleType: 1
    ResId: ""
    id: "cpzzacmtvphprdd0jmsha"
    isUnlock: true
    name: "导论"
    percent: 100
    sortOrder: 1]
    '''
    url = "https://mooc.icve.com.cn/study/learn/getCellByTopicId"
    data = {
        'courseOpenId': courseId,
        'topicId': topicId
    }
    result = json.loads(requests.post(url=url, data=data, headers=headers, cookies=cookies).text)
    return result['cellList']


# 5.拿到学习时长等信息---------->https://mooc.icve.com.cn/study/learn/viewDirectory?courseOpenId=wylwaxasdyjptaswj67x6g&cellId=qotwaxastizp0ktzqcnjg
def viewDirectory(cookies, courseOpenId, cellId):
    '''
    拿到学习时长等信息
    :param cookies: cookies
    :param courseOpenId: courseOpenId
    :param cellId: cellId
    :return: {'Id': 'cbwagosnyjooghaevg6fw', 'DateCreated': '/Date(1603976559000)/', 'CourseOpenId': 'gtjkawksy5jf7raso8gdq', 'TopicId': 'qc6vagosurpneukvl1nh1w', 'ParentId': 'qc6vagosly1owrpgpu6rg', 'CellName': '幼儿照护员的职业素养', 'CategoryName': 'ppt文档', 'CellType': 1, 'ResourceUrl': 'doc/g@85031789B2B47C2167D68CA0418D9FD3.pptx', 'ExternalLinkUrl': None, 'CellContent': None, 'RarJsonData': None, 'ztWay': 0, 'SpaceCount': 0, 'IsAllowDownLoad': False, 'KnowledgeIds': '', 'KnowledgeTitle': '', 'SortOrder': 1, 'FromType': 2, 'ImpProjectId': '', 'ImpProjectName': '', 'ImpDocId': '', 'ImpDocTitle': '', 'ResId': '', 'NewSortOrder': 0, 'FromId': None, 'VideoTimeLong': 0, 'DocSize': 9023286, 'PageCount': 8, 'DateModified': '/Date(-62135596800000)/', 'VideoQuestionCount': 0, 'PlayType': 0, 'FromMOOCCellId': '', 'DocId': 'cbwagosz7nmuxz8cxclg', 'GreenScan': 'pass', 'GreenScanScene': '', 'TableName': 'MOOC_CourseProcessCell'}
    '''
    time.sleep(1)
    url = "https://mooc.icve.com.cn/study/learn/viewDirectory"
    data = {
        'courseOpenId': courseOpenId,
        'cellId': cellId
    }
    result = requests.post(url=url, data=data, headers=headers, cookies=cookies)
    result = json.loads(result.text)
    return result['courseCell']


# 6.开始刷课--------->https://mooc.icve.com.cn/study/learn/statStuProcessCellLogAndTimeLong?courseOpenId=wylwaxasdyjptaswj67x6g&cellId=qotwaxastizp0ktzqcnjg&auvideoLength=487&videoTimeTotalLong=487
def statStuProcessCellLogAndTimeLong(cookies, courseOpenId, cellId, videoTimeTotalLong):
    '''
    开始刷课
    :param cookies: cookies
    :param courseOpenId: courseOpenId
    :param cellId: cellId
    :param videoTimeTotalLong: videoTimeTotalLong
    :return: {"code":1,"isStudy":true}
    '''
    time.sleep(2)
    url = "https://mooc.icve.com.cn/study/learn/statStuProcessCellLogAndTimeLong"
    data = {
        'courseOpenId': courseOpenId,
        'cellId': cellId,
        'auvideoLength': videoTimeTotalLong,
        'videoTimeTotalLong': videoTimeTotalLong
    }
    result = json.loads(requests.post(url=url, data=data, headers=headers, cookies=cookies).text)
    return result


def get_learn_time(cookies, courseOpenId, cellId):
    """
    获取学习时长
    :param cookies:
    :param courseOpenId:
    :param cellId:
    :return:
    """
    url = "https://mooc.icve.com.cn/study/learn/getLearnTime"
    data = {
        'courseOpenId': courseOpenId,
        'cellId': cellId
    }
    result = json.loads(requests.post(url=url, data=data, headers=headers, cookies=cookies).text)
    return result['learnTime']


def start():
    for key, value in get_user_all().items():
        cookies = login(key, value)  # 得到cookies用于后续登录
        course = getCourseOpenList(cookies)
        for i in course:
            time.sleep(1)
            if i['text'] == "国际商务谈判_第四次开课":  # 只刷 《国际商务谈判_第三次开课》这门课
                print("进入课程：" + i['text'])
            moduleList1 = getProcessList(cookies=cookies, courseId=i['id'])
            for j in moduleList1:
                time.sleep(0.25)
                print("\t" + j['name'])
            moduleList2 = getTopicByModuleId(cookies=cookies, courseId=i['id'], moduleId=j['id'])
            for k in moduleList2:
                time.sleep(0.25)
                print("\t\t" + k['name'])
                # 三级目录
                moduleList3 = getCellByTopicId(cookies=cookies, courseId=i['id'], topicId=k['id'])
                for m in moduleList3:
                    time.sleep(0.25)
                    print("\t\t\t" + m['cellName'])
    a = get_learn_time(cookies, course[0]['id'], course[0]['cellList'][0]['id'])
    print(a)


if __name__ == '__main__':
    start()
