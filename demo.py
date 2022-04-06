import csv


def get_user_all():
    """读取csv至字典"""
    csvFile = open("data.csv", "r")
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


for key, value in get_user_all().items():
    print("---------->正在读取{}的账号".format(key))
    data = {
        'userName': key,  # 账号
        'password': value,  # 密码
    }

if __name__ == '__main__':
    get_user_all()
