#!/usr/bin/env python
# coding: utf-8

import sys
import os
import time
import requests



tg_key = "аодываодывоалывдафывла"     
tg_url_bot_general = "https://api.telegram.org/bot"


def send_message(to, message):
    url = tg_url_bot_general + tg_key + "/sendMessage"
   # print(to)
  #  print(message)
   # message = "\n".join(message)
    params = {"chat_id": to, "text": message, "disable_web_page_preview": False,
                  "disable_notification": False}
    print(params)
    answer = requests.post(url, params=params, proxies=dict(http='socks5h://zabbix:пароль@айпи:5358',https='socks5h://zabbix:пароль@айпи:5358'), verify=False)
    if answer.status_code == 414:
        result = {"ok": False, "description": "414 URI Too Long"}
    else:
        result = answer.json()
    return result


def main():
    args = sys.argv
    to = args[1]
    message = args[2]
    send_message(to, message)
  #  print(send_message(to, message))
	
	
	
if __name__ == "__main__":
    main()