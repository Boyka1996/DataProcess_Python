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
