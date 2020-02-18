#!/usr/bin/env python3.6
# coding: utf-8


import json
import sys
import requests
import os
import base64
import smtplib
import datetime
import time

#Email settings
email_from = 'graylog@DOMEN'
email_username = ''
email_password = ''
email_smtp = '555.555.101.253'
email_smtp2 = '555.555.101.252'
#Template settings
company = 'АО "Компания"'
grl_tmp_path = '/var/tmp/grlemail'
grl_alert_path = '/usr/share/graylog-alert'


from jinja2 import Template

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

	
server_tmp_path = grl_tmp_path
server_alert_path = grl_alert_path

security_string = "123qweQWE"
iplisturl = "http://ДОмен/InternetBlockList.txt"
iplistphp = "http://Домен/blockInternetIp.php"



tg_key = "DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD"	 
tg_url_bot_general = "https://api.telegram.org/bot"

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

	def send(self):
		msg = MIMEMultipart("alternative")
		msg['Subject'] = self.mail_subject
		msg['From'] = self.mail_from
		msg['To'] = self.mail_to

		msg['X-Priority'] = self.mail_priority

		text = self.mail_body
		#text = "Dear Student" + "<br />" + "Fuck you!!"
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
		s.sendmail(self.mail_from, self.mail_to, msg.as_string())
		s.quit()


def send_message(to, message):
	url = tg_url_bot_general + tg_key + "/sendMessage"
	#print(to)
	#print(message)
	#message = "\n".join(message)
	params = {"chat_id": to, "text": message, "disable_web_page_preview": False,
				  "disable_notification": False}
	print(params)
	answer = requests.post(url, params=params, proxies=dict(http='socks5h://zabbix:password@IP:5358',https='socks5h://zabbix:password@IP:5358'), verify=False)
	if answer.status_code == 414:
		result = {"ok": False, "description": "414 URI Too Long"}
	else:
		result = answer.json()
	return result

	
	
def post_sec_audit(to, ip, message):
	url = to
	
	headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36"}
	
	data = '{"security_string":"' + security_string + '","ip":"'+ip+'","description":"'+message+'"}'
				  
	answer = requests.post(url, headers=headers, data=data, verify=False)
	
	
	
	print (answer.content.decode('utf-8'))
	
	
	
	result = ''
	
	
	if "Success" in answer.content.decode('utf-8'):
		result = "Адрес добавлен в список на блокировку."


	else:
		r = json.loads(answer.content.decode('utf-8'))
		result = "Адрес не добавлен в список на блокировку по следующей причине: " + r['result']

	return result

def send_api_3600():
	params = (
		('query', '(dst:77.236.230.* OR dst:212.73.99.* ) AND NOT (SecureXL AND Action:drop)'),
		('range', '3600'),
		('filter', 'streams:5ca8b5f32129b04c5c3202f4'),
		('field', 'src'),
		('order', 'src:desc'),
		('size', '50'),
		('stacked_fields', ''),
	)

	response = requests.get('https://555.555.100.208/api/search/universal/relative/terms', params=params, verify=False, auth=('bot', 'password'))

	for ip, count in  json.loads(response.text)['terms'].items():

		if count>= 1000 and ip!='IP':
			header = "\n🚩 Perimeter Scan Detected(more than 1000 in 1 hour)☝\n";   
			src_raw = ip
			src = "SRC: {0}\n".format(ip)
			ip_info = ''
			city = ''
			country = ''
			asprov = ''
			org = ''
			try:
				url = 'http://ip-api.com/json/' + ip
				src_info_json = json.loads((requests.get(url)).text)
				print(src_info_json)
				city = "city:" + src_info_json['city'] + "\n";
				print(city)
				country = "country:" + src_info_json['country'] + "\n";
				print(country)
				asprov = "as:" + src_info_json['as'] + "\n";
				print(asprov)
				org = "org:" + src_info_json['org'] + "\n";
				print(org)
			except:
				pass
			count = "count: {0}\n".format(count)
			ip_info = city+country+asprov+org
			send_message('-1001291345967',header +src +ip_info + count)
			body = 'Perimeter Scan Detected(more than 1000 in 1 hour) ' +src +ip_info + count
			r = post_sec_audit(iplistphp,src_raw,body)
			send_message('-1001291345967',"\n🚩 "+r+"☝\n")
			
			email = SendEmail()
			email.mail_from = email_from
			email.mail_user = email_username
			email.mail_pass = email_password
			email.mail_to = "securityinformation@DOMEN"
			email.mail_subject = "Perimeter Scan Detected(more than 1000 in 1 hour)"
			email.mail_body = "<br />".join((header +src +ip_info + count).split("\n"))
			email.mail_priority = '1'

			email.mail_server = email_smtp

			email.company = company
	


			email.send()
			email.mail_to = "yser1@DOMEN"
			email.send()
			email.mail_to = "user2@DOMEN"
			email.send()

			
			
			
			
			
			
   

def send_api_300():
	params = (
		('query', '(dst:77.236.230.* OR dst:212.73.99.* ) AND NOT (SecureXL AND Action:drop)'),
		('range', '300'),
		('filter', 'streams:5ca8b5f32129b04c5c3202f4'),
		('field', 'src'),
		('order', 'src:desc'),
		('size', '50'),
		('stacked_fields', ''),
	)

	response = requests.get('https://555.555.100.208/api/search/universal/relative/terms', params=params, verify=False, auth=('bot', 'password'))

	for ip, count in  json.loads(response.text)['terms'].items():

		if count>= 1000 and ip!='IP':
			header = "\n🚩 Intensvie Perimeter Scan Detected(more than 1000 in 5 minutes)☝\n";   
			src_raw = ip
			src = "SRC: {0}\n".format(ip)
			ip_info = ''
			city = ''
			country = ''
			asprov = ''
			org = ''
			try:
				url = 'http://ip-api.com/json/' + ip
				src_info_json = json.loads((requests.get(url)).text)
				print(src_info_json)
				city = "city:" + src_info_json['city'] + "\n";
				print(city)
				country = "country:" + src_info_json['country'] + "\n";
				print(country)
				asprov = "as:" + src_info_json['as'] + "\n";
				print(asprov)
				org = "org:" + src_info_json['org'] + "\n";
				print(org)
			except:
				pass
			count = "count: {0}\n".format(count)
			ip_info = city+country+asprov+org
			send_message('-1001291345967',header +src +ip_info + count)
			body = 'Intensvie Perimeter Scan Detected(more than 1000 in 5 minutes' + src +ip_info + count
			r = post_sec_audit(iplistphp,src_raw,body)
			send_message('-1001291345967',"\n🚩 "+r+"☝\n")
			
			email = SendEmail()
			email.mail_from = email_from
			email.mail_user = email_username
			email.mail_pass = email_password
			email.mail_to = "securityinformation@DOMEN"
			email.mail_subject = "Perimeter Scan Detected(more than 1000 in 1 hour)"
			email.mail_body = "<br />".join((header +src +ip_info + count).split("\n"))
			email.mail_priority = '1'

			email.mail_server = email_smtp

			email.company = company
	

			email.send()


			email.mail_to = "gudkovab@DOMEN"
			email.send()
			email.mail_to = "voskresenskijas@DOMEN"
			email.send()
	


def send_api_ip():
	params = (
		('query', '(dst:77.236.230.* OR dst:212.73.99.*) AND (185.61.138.249 OR src:185.162.131.97 OR src:91.192.100.62 OR src:212.8.240.116 OR src:168.167.45.162, 5.178.83.122 OR src:5.178.83.123 OR src:88.198.38.187 OR src:94.159.6.254 OR src:77.246.144.113 OR src:162.243.211.124, 195.123.228.208 OR src:188.165.200.156 OR src:120.192.73.202 OR src:180.182.52.76 OR src:5.88.164.18, 151.54.18.54 OR src:185.102.136.141 OR src:185.239.50.242 OR src:185.102.136.132 OR src:185.176.27.246, 185.176.27.166 OR src:185.176.27.162 OR src:185.176.27.50 OR src:185.176.27.42 OR src:188.165.200.156, 185.203.116.89 OR src:185.205.210.233 OR src:188.165.200.156 OR src:185.205.210.233 OR src:185.203.116.89, 217.12.223.59 OR src:188.165.200.156 OR src:188.165.200.233 OR src:91.217.137.37 OR src:217.12.210.54, 185.104.29.62 OR src:86.59.21.38 OR src:208.83.223.34 OR src:34.83.76.33 OR src:171.25.193.9 OR src:154.35.32.5, 185.77.129.35 OR src:5.9.143.167 OR src:185.61.149.186 OR src:188.165.200.156 OR src:185.205.210.233, 185.203.116.89 OR src:109.234.165.77 OR src:79.134.235.253 OR src:24.93.21.157 OR src:62.210.213.17, 185.85.15.31 OR src:54.192.13.204 OR src:162.243.211.124 OR src:188.165.200.156 OR src:185.205.210.233, 173.223.103.88 OR src:104.16.155.36 OR src:104.18.34.131 OR src:128.31.0.39 OR src:163.172.53.201 OR src:171.25.193.9, 185.96.180.29 OR src:195.154.165.64 OR src:54.38.92.43 OR src:76.73.17.194 OR src:85.214.141.131 OR src:85.229.166.15, 85.217.170.12 OR src:91.92.136.57 OR src:217.12.210.54 OR src:91.217.137.37 OR src:188.165.200.156, 185.247.228.248 OR src:85.217.170.12 OR src:91.92.136.57 OR src:217.12.210.54 OR src:91.217.137.37, 188.165.200.156 OR src:162.243.211.124 OR src:185.205.210.233 OR src:85.217.170.12 OR src:91.92.136.57, 217.12.210.54 OR src:91.217.137.37 OR src:188.165.200.156 OR src:59.110.185.163 OR src:94.156.35.33, 104.25.47.99 OR src:185.70.186.151 OR src:185.70.186.149 OR src:91.92.136.57 OR src:169.239.129.60, 169.239.129.61 OR src:104.25.48.99 OR src:104.25.47.99 OR src:212.73.150.110 OR src:104.25.47.99 OR src:104.25.48.99, 212.73.150.189 OR src:85.217.170.12)'),
		('range', '3600'),
		('filter', 'streams:5ca8b5f32129b04c5c3202f4'),
		('field', 'src'),
		('order', 'src:desc'),
		('size', '50'),
		('stacked_fields', ''),
	)

	response = requests.get('https://555.555.100.208/api/search/universal/relative/terms', params=params, verify=False, auth=('bot', 'password'))
	print(response.text)
	for ip, count in  json.loads(response.text)['terms'].items():

		if count>= 1 and ip!='IP':
			header = "\n🚩 Обнаружена активность от адресов из списка ЦКЗ (60 минутный интервал )☝\n";   
			src = "SRC: {0}\n".format(ip)
			ip_info = ''
			city = ''
			country = ''
			asprov = ''
			org = ''
			try:
				url = 'http://ip-api.com/json/' + ip
				src_info_json = json.loads((requests.get(url)).text)
				print(src_info_json)
				city = "city:" + src_info_json['city'] + "\n";
				print(city)
				country = "country:" + src_info_json['country'] + "\n";
				print(country)
				asprov = "as:" + src_info_json['as'] + "\n";
				print(asprov)
				org = "org:" + src_info_json['org'] + "\n";
				print(org)
			except:
				pass
			count = "count: {0}\n".format(count)
			ip_info = city+country+asprov+org
			send_message('-1001291345967',header +src +ip_info + count)
			
			email = SendEmail()
			email.mail_from = email_from
			email.mail_user = email_username
			email.mail_pass = email_password
			email.mail_to = "securityinformation@DOMEN"
			email.mail_subject = "Обнаружена активность от адресов из списка ЦКЗ (60 минутный интервал)"
			email.mail_body = "<br />".join((header +src +ip_info + count).split("\n"))
			email.mail_priority = '1'

			email.mail_server = email_smtp

			email.company = company
	

			email.send()
			email.mail_to = "gudkovab@DOMEN"
			email.send()
			email.mail_to = "voskresenskijas@DOMEN"
			email.send()

	
		
def main():
	args = sys.argv
	arg = args[1]
	if arg == '3600':
		send_api_3600()
	if arg == '300':
		send_api_300()
	if arg == 'ip':
		send_api_ip()


	
	
	
if __name__ == "__main__":
	main()
		
		