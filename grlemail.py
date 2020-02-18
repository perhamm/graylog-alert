#!/usr/bin/env python
# coding: utf-8
import grlemail_settings
import sys
import requests
import os
import base64
import smtplib
import sys
import base64
import datetime
import time
import re

from jinja2 import Template

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

	
server_tmp_path = grlemail_settings.grl_tmp_path
server_alert_path = grlemail_settings.grl_alert_path


class SendEmail(object):
	"""docstring for SendEmail"""
	def __init__(self):
		super(SendEmail, self).__init__()
		self.mail_from = ''
		self.mail_user = ''
		self.mail_to = ''
		self.mail_server = ''
		self.mail_pass = ''
		self.mail_subject = ''
		self.mail_body = ''
		self.mail_priority = ''
		self.mail_cc = ''
		self.mail_bcc = ''

	def send(self):
		msg = MIMEMultipart("alternative")
		msg['Subject'] = self.mail_subject
		msg['From'] = self.mail_from
		msg['To'] = self.mail_to
		msg['Cc'] = self.mail_cc
		msg['X-Priority'] = self.mail_priority

		text = self.mail_body.decode('utf-8')

		#print(text)
		

		
		template_file = open(server_alert_path + '/email_template.j2')
		template_text = ''
		for lines in template_file:
			template_text = template_text + lines

		t = Template(template_text)
		
		
	
		
		html = t.render(alert_text=text)

		
		part1 = MIMEText(html, 'html', 'utf-8')
		

		msg.attach(part1)

		

		s = smtplib.SMTP()
		s.connect(self.mail_server)
		s.ehlo(self.mail_from)
		#s.login(self.mail_user, self.mail_pass)
		s.sendmail(self.mail_from, [self.mail_to] + self.mail_cc.split(",") + self.mail_bcc.split(","), msg.as_string())
		s.quit()


def parse_email(body):
	
	match = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", body)
	print(match)
	senderto = match[1]
	return senderto
	
		
def main():
	
		
	email = SendEmail()

	type = sys.argv[1]
	body = sys.argv[2]
	
	print (body)
	

	email.mail_from = grlemail_settings.email_from
	email.mail_user = grlemail_settings.email_username
	email.mail_pass = grlemail_settings.email_password
	if type == "spam":
	
		email.mail_from = "KasperskyAntiSpam@DOMEN"
		email.mail_subject = "Blocked messages by Kaspersky AntiSpam"
		
		email.mail_priority = '5'
		email.mail_server = grlemail_settings.email_smtp
		email.company = grlemail_settings.company

		emailto = parse_email(body)
		header = '''<table class=MsoNormalTable border=1 cellspacing=0 cellpadding=0
 style='border-collapse:collapse;border:none;mso-border-alt:dashed red .75pt;
 mso-yfti-tbllook:1184'>
 <tr style='mso-yfti-irow:0;mso-yfti-firstrow:yes;mso-yfti-lastrow:yes'>
  <td style='border:dashed red 1.0pt;mso-border-alt:dashed red .75pt;
  padding:.75pt .75pt .75pt .75pt'>
  <p class=MsoNormal><span style='font-family:"Arial",sans-serif;mso-fareast-font-family:
  "Times New Roman";color:red'>Внимание. Это сообщение поступило НЕ с адреса
  организации системы &quot;ИМЯКОМПАНИИ&quot;.<br>Оно было отмечено системой как спам, а также преобразовано.</span><span style='font-family:
  "Arial",sans-serif;mso-fareast-font-family:"Times New Roman"'> <br>
  <u>В случае, если Вы считаете что данное сообщение было ошибочно отмечено как спам,<br>просьба обратится в техническую поддержку локальных ИТ-систем для восстановления письма. </u> <o:p></o:p></span></p>
  </td>
 </tr>
</table>'''
		text = "<br />".join(body.split("|"))
		text = text.replace('kavscmesrv.exe','')
		email.mail_body = header + text
		email.mail_to = emailto
		email.mail_cc = "User231231@DOMEN"
		email.mail_bcc = "USer1@DOMEN,USer12@DOMEN,USer1333@DOMEN"
		email.send()
		



if __name__ == "__main__":
	main()
