#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
import smtplib
import config
from email.mime.text import MIMEText
from email.utils import formataddr

class MailApi():
    def __init__(self, sender, sender_name, sender_password, smtp_url, smtp_ssl_port) -> None:
        """
        :param sender: 发件人 str
        :param sender_name: 发件人姓名 str
        :param sneder_password: 发件密码 str
        :param smtp_url: smtp的域名
        :param smtp_ssl_port: smtp ssl 端口
        """
        self.sender = sender
        self.sender_name = sender_name
        self.sender_password = sender_password
        self.smtp_url = smtp_url
        self.smtp_ssl_port = smtp_ssl_port

        self.server=smtplib.SMTP_SSL(smtp_url, smtp_ssl_port)  # 发件人邮箱中的SMTP服务器，端口是25
        self.server.login(sender, sender_password)  # 括号中对应的是发件人邮箱账号、邮箱密码

    def send_mail(self, receivers, subject, mail_msg):
        """
        :param receivers: 收件人列表 a@qq.com,b@qq.com
        """
        try:
            msg=MIMEText(mail_msg,'html','utf-8')
            msg['From']=formataddr([self.sender_name, self.sender])  
            msg['To']=receivers            
            msg['Subject']=subject
            self.server.sendmail(self.sender, msg['To'].split(','), msg.as_string())
            print("发送成功")
        except Exception as e:
            print("发送失败", e)



if __name__ == "__main__":
    exmailObj = MailApi(sender=config.get_config("global", "sender"),
                        sender_name=config.get_config("global", "sender_name"),
                        sender_password=config.get_config("global", "sender_password"),
                        smtp_url=config.get_config("global", "smtp_url"),
                        smtp_ssl_port=config.get_config("global", "smtp_ssl_port"))

    # 第一封邮件
    subject = config.get_config("mail", "subject")
    mail_msg = config.get_config("mail", "mail_msg")
    receivers = config.get_config("mail", "receivers")
    exmailObj.send_mail(receivers=receivers, subject=subject, mail_msg=mail_msg)

    # # 第二封邮件
    # subject = "测试邮件标题444"
    # mail_msg = """
    # <p>我帅不帅444</p>
    # <p><a href="http://www.runoob.com">测试测试测试</a></p>
    # """
    # receivers = ["iuxt@qq.com", "yong.wang@ingeek.com"]
    # exmailObj.send_mail(receivers=receivers, subject=subject, mail_msg=mail_msg)

    # 发送完邮件, 关闭连接
    exmailObj.server.quit()