import os
import sys
import psycopg2
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pyimgur
import json
import requests
from bs4 import BeautifulSoup
from youtube_search import YoutubeSearch

from transitions.extensions import GraphMachine

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, ImageSendMessage

from utils import send_text_message

import template

mpl.rcParams[u'font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False

DATABASE_URL = os.environ['DATABASE_URL']
#DATABASE_URL = os.popen('heroku config:get DATABASE_URL -a toc-final-project').read()[:-1]
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
cursor.execute(f"""SELECT * FROM account_table""", )
data = []
while True:
    temp = cursor.fetchone()
    if temp:
        data.append(temp)
    else:
        break
print(data)


now_type = ''
now_money = 0
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_mainmenu(self, event):
        text = event.message.text
        return text == "主選單"

    def is_going_to_introduction(self, event):
        text = event.message.text
        return text == "功能介紹"

    def is_going_to_keep_accounts(self, event):
        text = event.message.text
        return text == "記帳"

    def is_going_to_spending_mode(self, event):
        text = event.message.text
        return text == "支出"
    def is_going_to_earning_mode(self, event):
        text = event.message.text
        return text == "收入"

    def is_going_to_enter_spending(self, event):
        global now_type, now_money
        text = event.message.text
        t = text.split()
        if len(t) != int(3):
            return False
        elif t[0].isnumeric():
            now_type = t[1]
            now_money = t[0]
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()
            if len(t[2]) != 0:
                record = (str(event.source.user_id), 'True', t[0], t[1], t[2])
            else: 
                record = (str(event.source.user_id), 'True', t[0], t[1], '無')
            table_columns = '(user_id, recoord_type, money, money_type, money_description)'
            postgres_insert_query = f"""INSERT INTO account_table {table_columns} VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(postgres_insert_query, record)
            conn.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into account_table")
            cursor.close()
            conn.close()
            return True
        return False
    def is_going_to_enter_earning(self, event):
        global now_type, now_money
        text = event.message.text
        t = text.split()
        if len(t) != int(3):
            return False
        elif t[0].isnumeric():
            now_type = t[1]
            now_money = t[0]
            conn = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = conn.cursor()
            if len(t[2]) != 0:
                record = (str(event.source.user_id), 'False', t[0], t[1], t[2])
            else: 
                record = (str(event.source.user_id), 'False', t[0], t[1], '無')
            table_columns = '(user_id, recoord_type, money, money_type, money_description)'
            postgres_insert_query = f"""INSERT INTO account_table {table_columns} VALUES (%s, %s, %s, %s, %s);"""
            cursor.execute(postgres_insert_query, record)
            conn.commit()
            count = cursor.rowcount
            print(count, "Record inserted successfully into account_table")
            cursor.close()
            conn.close()
            return True
        return False
    def is_going_to_watch_all_record(self, event):
        text = event.message.text
        return text == "查看所有紀錄"
    def is_going_to_edit(self, event):
        text = event.message.text
        return text == "編輯"
    def is_going_to_edit_data(self, event):
        text = event.message.text
        s = text.split(',')
        t=[]
        for i in range(len(s)) :
            ss = s[i].split()
            t.append(ss[0])
            t.append(ss[1])
        if len(t) % 2 != 0 :
            return False
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        for i in range(0, len(t), 2) :
            if t[i] == '價錢' :
                cursor.execute(f"""UPDATE account_table SET money = %s WHERE num_id = (select max(num_id) from account_table);""", (t[i+1],))
            elif t[i] == '分類' :
                cursor.execute(f"""UPDATE account_table SET money_type = %s WHERE num_id = (select max(num_id) from account_table)""", (t[i+1],))
            elif t[i] == '說明' :
                cursor.execute(f"""UPDATE account_table SET money_description = %s WHERE num_id = (select max(num_id) from account_table)""", (t[i+1],))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def is_going_to_watch_chart(self, event):
        text = event.message.text
        return text == "查看收支圖表"

    def is_going_to_watch_balance(self, event):
        text = event.message.text
        return text == "本月目前結餘"

    def is_going_to_watch_video(self, event):
        text = event.message.text
        return text == "觀看影片"

    def is_going_to_show_fsm(self, event):
        text = event.message.text
        return text == "查看fsm diagram"

    def on_enter_mainmenu(self, event):
        reply_token = event.reply_token
        message = template.main_menu
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
    '''
    def on_enter_introduction(self, event):
        reply_token = event.reply_token
        message = template.introduction_message
        message_to_reply = FlexSendMessage("開啟功能介紹", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()
    '''
    def on_enter_keep_accounts(self, event):
        reply_token = event.reply_token
        message = template.se_type
        message_to_reply = FlexSendMessage("開啟記帳功能", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_spending_mode(self, event):
        send_text_message(event.reply_token, '請輸入支出的資料(價錢 分類 說明), ex:5 飲食 午餐')
    def on_enter_earning_mode(self, event):
        send_text_message(event.reply_token, '請輸入收入的資料(價錢 分類 說明), ex:10 零用錢 媽媽10塊')
    def on_enter_enter_spending(self, event):
        total = 0
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM account_table where (user_id = %s AND money_type = %s)""", (event.source.user_id, now_type))
        while True:
            temp = cursor.fetchone()
            if temp:
                if temp[2] == True:
                    total += int(temp[3])
            else:
                break
        reply_token = event.reply_token
        message = template.enter_success
        message["body"]["contents"][0]["text"] = "已在 " + now_type + "類 加上   " + now_money + "元"
        message["body"]["contents"][1]["text"] = "本月 " + now_type + "類 已經累計 " + str(total) + "元"
        message_to_reply = FlexSendMessage("輸入成功！", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
    def on_enter_enter_earning(self, event):
        total = 0
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM account_table where (user_id = %s AND money_type = %s)""", (event.source.user_id, now_type))
        while True:
            temp = cursor.fetchone()
            if temp:
                if temp[2] == False:
                    total += int(temp[3])
            else:
                break
        reply_token = event.reply_token
        message = template.enter_success
        message["body"]["contents"][0]["text"] = "已在 " + now_type + "類 加上   " + now_money + "元"
        message["body"]["contents"][1]["text"] = "本月 " + now_type + "類 已經累計 " + str(total) + "元"
        message_to_reply = FlexSendMessage("輸入成功！", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
    def on_enter_watch_all_record(self, event):
        s_list = []
        e_list = []
        msg_s = ''
        msg_e = ''
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM account_table where user_id = %s""", (event.source.user_id,))
        while True:
            temp = cursor.fetchone()
            if temp:
                if temp[2]  == True:
                    s_list.append(temp[0])
                    msg_s += str(len(s_list)) + temp[4] + "\t" + str(temp[3]) + "\t" + temp[5] + '\n'
                elif temp[2]  == False:
                    e_list.append(temp[0])
                    msg_e += temp[4] + "\t" + str(temp[3]) + "\t" + temp[5] + '\n'
            else:
                break
        send_text_message(event.reply_token, msg_s + '\n' + msg_e + '\n' + "請輸入'主選單'來回到主選單")
        self.go_back()

    def on_enter_edit(self, event):
        send_text_message(event.reply_token, '請輸入要修改的部份(價錢 分類 說明), ex:價錢 5,分類 娛樂, 說明 晚餐')
    def on_enter_edit_data(self, event):
        reply_token = event.reply_token
        message = template.edit_success
        message_to_reply = FlexSendMessage("輸入成功！", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_watch_chart(self, event):
        s_list = {}
        e_list = {}
        total_s = 0
        total_e = 0
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM account_table where user_id = %s""", (event.source.user_id,))
        while True:
            temp = cursor.fetchone()
            if temp:
                if temp[2] == True:
                    if temp[4] in s_list:
                        s_list[temp[4]] += int(temp[3])
                    else:
                        s_list[temp[4]] = int(temp[3])
                    total_s += int(temp[3])
                elif temp[2] == False:
                    if temp[4] in e_list:
                        e_list[temp[4]] += int(temp[3])
                    else:
                        e_list[temp[4]] = 0
                    total_e += int(temp[3])
            else:
                break
        labels = []
        sizes = []
        msg = "支出 :\n"
        for x, y in s_list.items():
            msg += str(x) + '\t' + str(y) + '\n'
            labels.append(x)
            sizes.append(y)
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')
        plt.savefig('chart_s.png', dpi=300)
        plt.close()
        labels.clear()
        sizes.clear()
        msg += "\n收入 :\n"
        for x, y in e_list.items():
            msg += str(x) + '\t' + str(y) + '\n'
            labels.append(x)
            sizes.append(y)
        msg += "\n請輸入'主選單'來回到主選單"
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.axis('equal')
        plt.savefig('chart_e.png', dpi=300)
        plt.close()
    
        CLIENT_ID = "fe5468cf1e4d868"
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image_s = im.upload_image("chart_s.png", title="upload")
        uploaded_image_e = im.upload_image("chart_e.png", title="upload")        
        
        reply_token = event.reply_token
        message_to_reply = []
        message_to_reply.append(ImageSendMessage(original_content_url=uploaded_image_s.link, preview_image_url=uploaded_image_s.link))
        message_to_reply.append(ImageSendMessage(original_content_url=uploaded_image_e.link, preview_image_url=uploaded_image_e.link))
        message_to_reply.append(TextSendMessage(msg))
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_watch_balance(self, event):
        total_s = 0
        total_e = 0
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM account_table where user_id = %s""", (event.source.user_id,))
        while True:
            temp = cursor.fetchone()
            if temp:
                if temp[2] == True:
                    total_s += int(temp[3])
                elif temp[2] == False:
                    total_e += int(temp[3])
            else:
                break
        dif = total_e-total_s
        reply_token = event.reply_token
        message = template.shiba_bar
        if dif < 0 :
            message["body"]["contents"][0]["url"] = "https://i.imgur.com/xZAfcmu.png"
        elif dif > 0 :
            message["body"]["contents"][0]["url"] = "https://i.imgur.com/9Gb5Gtp.png"
        message["body"]["contents"][2]["contents"][0]["text"] = "$" + str(total_s)
        message["body"]["contents"][2]["contents"][1]["text"] = "$" + str(dif)
        message["body"]["contents"][2]["contents"][2]["text"] = "$" + str(total_e)
        message_to_reply = FlexSendMessage("開啟結餘", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_watch_video(self, event):
        url = 'https://www.youtube.com/results?search_query=funny+dog'
        url_list = []
        img_list = []
        title_list = []
        results = YoutubeSearch('funny dog', max_results=10).to_dict()
        print(results[0])
        for i in range(5):
            url_list.append('https://www.youtube.com/watch?v=' + results[i]['id'])
            img_list.append(results[i]['thumbnails'][0])
            title_list.append(results[i]['title'])
        '''
        for i in range(5):
            #url_list.append('https://www.youtube.com' + soup.select('.yt-lockup-video')[i].select("a[rel='spf-prefetch']")[0].get("href"))
            print(url_list[i])
            img_list.append(soup.select('.yt-lockup-video')[i].select('img')[0].get('src'))
        '''
        reply_token = event.reply_token
        message = template.yt_video
        for i in range(5) :
            message["contents"][i]["hero"]["url"] = str(img_list[i])
            message["contents"][i]["body"]["contents"][0]["text"] = str(title_list[i])
            message["contents"][i]["footer"]["contents"][0]["action"]["uri"] = url_list[i]
        message_to_reply = FlexSendMessage("觀看影片", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_show_fsm(self, event):
        reply_token = event.reply_token
        message_to_reply = ImageSendMessage(original_content_url='https://i.imgur.com/yhzB3eA.png', preview_image_url='https://i.imgur.com/yhzB3eA.png')
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()