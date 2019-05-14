#encoding=utf-8
import xlrd
import time
import datetime
import os
import re

def parser_class_all(filepath):
    if not os.path.exists(filepath):
        return None
    workbook = xlrd.open_workbook(filepath)
    sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    classes={}
    for i in range(4,sheet.nrows):
        try:
            for j in range(1, sheet.ncols):
                # 班级号
                class_name = sheet.cell(i, 0).value
                if class_name not in classes:
                    classes[class_name] = {}
                t = sheet.cell(i, j).value.strip()
                if len(t) <= 0:
                    continue

                class_cells_infos = re.findall("(.*?)\\[\\d+-\\d+节\\]", t, re.S)
                for info in class_cells_infos:
                    info = info.strip()
                    infos = info.split("\n")
                    # print(repr(infos[-1]))
                    course_name = infos[0]
                    if course_name not in classes[class_name]:
                        classes[class_name][course_name] = []
                    week_day = sheet.cell(2, j).value
                    course_ind = sheet.cell(3, j).value
                    index_2_num = {v: i + 1 for i, v in enumerate("一	二	三	四	五".split("\t"))}
                    weekday_2_num = {v: i + 1 for i, v in enumerate("周一	周二	周三	周四	周五".split("\t"))}

                    course_weeks = parse_weeks(infos[-1][1:-1])
                    week_day = weekday_2_num[week_day]
                    course_ind = index_2_num[course_ind]

                    classes[class_name][course_name].append({
                        "weeks": course_weeks,
                        "week_day": week_day,
                        "course_ind": course_ind
                    })

        except Exception as e:
            print(e)

    return classes

def parse_weeks(week_str):
    result =[]
    for item in week_str.split(","):
        m = re.match("^(\\d+)-(\\d+)$", item)
        if m:
            start = int(m.group(1))
            end = int(m.group(2))
            result.extend([i for i in range(start,end+1)])
            continue
        m = re.match("^(\\d+)-(\\d+)周$", item)
        if m:
            start = int(m.group(1))
            end = int(m.group(2))
            result.extend([i for i in range(start, end + 1)])
            continue
        m = re.match("^单周$", item)
        if m:
            res = [x for x in result if x%2 ==1]
            result = res
            continue
        m = re.match("^双周$", item)
        if m:
            res = [x for x in result if x % 2 == 0]
            result = res
            continue
        m = re.match("^(\\d+)周$", item)
        if m:
            start = int(m.group(1))
            result.append(start)
            continue
        m = re.match("^(\\d+)$", item)
        if m:
            start = int(m.group(1))
            result.append(start)
            continue
        print("不能解析",week_str)
        assert  False == True
    return result

def parse_config(filepath):
    if not os.path.exists(filepath):
        return None
    workbook = xlrd.open_workbook(filepath)
    sheet = workbook.sheet_by_index(0)  # sheet索引从0开始
    #students=[]
    rooms={}

    for i in range(1,sheet.nrows):
        try:
            room_id = str(int(sheet.cell(i, 1).value))
            if room_id not in rooms:
                rooms[room_id]=[]
            item = {
                "chair_id": int(sheet.cell(i, 0).value),
                "name": sheet.cell(i, 2).value.strip(),
                "class": sheet.cell(i, 3).value.strip(),
            }
            rooms[room_id].append(item)
        except Exception as e:
            print(e)

    return rooms




if __name__ == "__main__":
    import json
    #classes = parser_class_all("docs/classes_all.xls")
    #print(json.dumps(classes))
    #res = parse_weeks("5-18周,单周")
    #print(res)
    students = parse_config("docs/新建 Microsoft Excel 工作表.xlsx")
    print(students)