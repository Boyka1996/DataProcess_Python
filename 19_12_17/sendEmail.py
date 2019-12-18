# !/usr/bin/python3
import smtplib
from email.mime.text import MIMEText

msg_from = '***@163.com'
passward = '***' #授权码
msg_to = '***@qq.com'

subject = '这是测试邮件'
content = '这是用python和smtp模块发送的邮件'

msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

try:
    s = smtplib.SMTP('smtp.163.com',25)
    s.login(msg_from,passward)
    s.sendmail(msg_from,msg_to,msg.as_string())
    print('发送成功')
except smtplib.SMTPException as e:
    print('发送失败' + format(e))
finally:
    s.quit()
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# # 第三方 SMTP 服务
# mail_host = "smtp.163.com"  # 设置服务器
# mail_user = "upcvagen@163.com"  # 用户名
# mail_pass = "19960721zhao"  # 口令
#
# sender = 'from@runoob.com'
# receivers = ['1292549471@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
#
# message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
# message['From'] = Header("菜鸟教程", 'utf-8')
# message['To'] = Header("测试", 'utf-8')
#
# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')
#
# try:
#     smtpObj = smtplib.SMTP()
#     smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
#     smtpObj.login(mail_user, mail_pass)
#     print(111)
#     smtpObj.sendmail(sender, receivers, message.as_string())
#     print("邮件发送成功")
# except smtplib.SMTPException:
#     print("Error: 无法发送邮件")
