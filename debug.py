import csv


def read():
    with open('data/1.csv', 'r', encoding='gbk') as csvf:
        csvrf = csv.reader(csvf)  # 获取read权限的csv对象
        for i in csvrf:
            if csvrf.line_num == 1:
                continue
            print(i)


def write():
    with open('data/2.csv', 'w', encoding='gbk', newline='') as csvf:
        csvwf = csv.writer(csvf, dialect='excel')  # 获取允许写的指定文件对象，并设置默认打开方式为excel
        csvwf.writerow(['A', 'B', 'C', 'D'])  # 直接写入会存在空行——应该在打开时添加newline="",否则默认是"\n"
        csvwf.writerow(['1', '3', '5', '8'])  # 行写入



if __name__ == '__main__':
    read()
    write()
