import requests
import json
import datetime
import time
import random

# 这玩意获取学生基本信息的网址实际上是 https://app.upc.edu.cn/uc/api/oauth/index?redirect=http://stu.gac.upc.edu.cn:8089/xswc&appid=200200819124942787&state=2
# 剩下的前端根本不验证你的 Cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://stu.gac.upc.edu.cn:8089',
    'Connection': 'keep-alive',
    'Referer': 'http://stu.gac.upc.edu.cn:8089/xswc?code=1b5b4e868072bf0a51655aff7521f681&state=2',
}
base = datetime.datetime.today()
# data = {
#   'stuXh': 'S18070028', # 学号
#   'stuXm': '赵宏伟', # 姓名
#   'stuXy': '计算机科学与技术学院', # 学院
#   'stuZy': '软件工程', # 专业
#   'stuMz': '汉', # 民族
#   'stuBj': '研1801', # 班级
#   'stuLxfs': '17854227883', # 联系方式
#   'stuJzdh': '13563660282', # 家长电话
#   'stuJtfs': '公交', # 交通方式
#   'stuStartTime': '', # 外出时间，可以自动生成，无需填写
#   'stuReason': '购物', # 外出事由
#   'stuWcdz': '南门', # 外出地址（仅限青岛市）
#   'stuJjlxr': '李兆桐', # 外出紧急联系人
#   'stuJjlxrLxfs': '17854227901' # 紧急联系人联系方式
#   # 至于这个本人承诺，纯粹只是把验证放到前端去了
# }
data = {
  'stuXh': 'M18070007', # 学号
  'stuXm': '尹广楹', # 姓名
  'stuXy': '计算机科学与技术学院', # 学院
  'stuZy': '计算机技术', # 专业
  'stuMz': '汉', # 民族
  'stuBj': '研1804', # 班级
  'stuLxfs': '17854227883', # 联系方式
  'stuJzdh': '13563660282', # 家长电话
  'stuJtfs': '公交', # 交通方式
  'stuStartTime': '', # 外出时间，可以自动生成，无需填写
  'stuReason': '购物', # 外出事由
  'stuWcdz': '南门', # 外出地址（仅限青岛市）
  'stuJjlxr': '李兆桐', # 外出紧急联系人
  'stuJjlxrLxfs': '17854227901' # 紧急联系人联系方式
  # 至于这个本人承诺，纯粹只是把验证放到前端去了
}

dataJtfs = {
    '1': '步行',
    '2': '公交',
    '3': '打车'
}

dataReason = {
    '1': '购物',
    '2': '聚餐',
    '3': '娱乐',
    '4': '买东西'
}

dataWcdz = {
    '1': '青岛市'
}

def AbsentReq(days):
    date_list = [base + datetime.timedelta(days=x) for x in range(days)]
    dates = [x.strftime("%Y-%m-%d") + ' 03:00:00' for x in date_list]
    for i in dates:
        jtfs = random.sample(dataJtfs.keys(), 1)    # 随机理由
        reason = random.sample(dataReason.keys(), 1)
        wcdz = random.sample(dataWcdz.keys(),1)
        data['stuJtfs'] = dataJtfs.get(jtfs[0])
        data['stuReason'] = dataReason.get(reason[0])
        data['stuWcdz'] = dataWcdz.get(wcdz[0])
        data['stuStartTime'] = i
        response = requests.post('http://stu.gac.upc.edu.cn:8089/stuqj/addQjMess', headers=headers, data=data)
        if response.json()['resultStat'] == "success":
            print('请假时间为 {} 的请假已成功.'.format(data['stuStartTime']))
            print('今天的请假理由是{}去{}{}'.format(data['stuJtfs'], data['stuWcdz'], data['stuReason']))
        else:
            print('请假失败，原因:{}'.format(response.json()['mess']))
    # 返回值
    # 重复提交：{"resultStat":"error","mess":"您2021-03-16的请假信息已提交，请勿重复添加。","data":null,"othermess":null}
    # 成功提交：{"resultStat":"success","mess":"成功","data":1,"othermess":null}
    # 提交错误2：{"resultStat":"error","mess":"添加请假信息异常","data":"String index out of range: 10","othermess":null}
if __name__ == '__main__':
    print("在请假之前，请先确保你已经把正确的信息填入了源代码中，否则请假将无法完成!")
    days = int(input("请输入要请假的天数："))
    AbsentReq(days)
    print('请假{}天已成功，10秒后退出...'.format(days))
    time.sleep(10)
