import os
import sys
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
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, TemplateSendMessage, ImageCarouselColumn, ImageCarouselTemplate, URITemplateAction

from utils import send_text_message

import template

mpl.rcParams[u'font.sans-serif'] = ['simhei']
mpl.rcParams['axes.unicode_minus'] = False

spend_list = []
spend_list_tog = {}
earn_list = []
earn_list_tog = {}
spend_type = ['飲食', '日常', '交通', '娛樂', '醫療']
earn_type = ['薪水', '零用錢']
se_mode = -1

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
        global se_mode
        se_mode = 0
        text = event.message.text
        t = text.split()
        if len(t) != int(3):
            return False
        elif t[0].isnumeric() and t[1] in spend_type:
            spend_list.append(dict(spend_type = t[1], spend_money = t[0], description = t[2]) )
            return True
        elif t[0].isnumeric() :
            spend_type.append(t[1])
            spend_list.append(dict(spend_type = t[1], spend_money = t[0], description = t[2]) )
            return True
        return False
    def is_going_to_enter_earning(self, event):
        global se_mode
        se_mode = 1
        text = event.message.text
        t = text.split()
        if len(t) != int(3) :
            return False
        elif t[0].isnumeric() and t[1] in earn_type :
            earn_list.append(dict(earn_type = t[1], earn_money = t[0], description = t[2]) )
            return True
        elif t[0].isnumeric() :
            earn_type.append(t[1])
            earn_list.append(dict(earn_type = t[1], earn_money = t[0], description = t[2]) )
            return True
        return False
    def is_going_to_edit(self, event):
        text = event.message.text
        return text == "編輯"
    def is_going_to_edit_data(self, event):
        global se_mode
        text = event.message.text
        s = text.split(',')
        t=[]
        for i in range(len(s)) :
            ss = s[i].split()
            t.append(ss[0])
            t.append(ss[1])
        if len(t) % 2 != 0 :
            return False
        for i in range(0, len(t), 2) :
            if t[i] == '價錢' :
                if se_mode == 0 :
                    t[i] = 'spend_money'
                elif se_mode == 1 :
                    t[i] = 'earn_money'
            elif t[i] == '分類' :
                if se_mode == 0 :
                    t[i] = 'spend_type'
                elif se_mode == 1 :
                    t[i] = 'earn_type'
            elif t[i] == '說明' :
                t[i] = 'description'
            if se_mode == 0 :
                spend_list[-1][t[i]] = t[i+1]
            elif se_mode == 1 :
                earn_list[-1][t[i]] = t[i+1]
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
        reply_token = event.reply_token
        message = template.enter_success
        total = 0
        for i in range(len(spend_list)) :
            if spend_list[i]['spend_type'] == spend_list[-1]['spend_type'] :
                total += int(spend_list[i]['spend_money'])
        message["body"]["contents"][0]["text"] = "已在 " + spend_list[-1]['spend_type'] + "類 加上   " + spend_list[-1]['spend_money'] + "元"
        message["body"]["contents"][1]["text"] = "本月 " + spend_list[-1]['spend_type'] + "類 已經累計 " + str(total) + "元"
        message_to_reply = FlexSendMessage("輸入成功！", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
    def on_enter_enter_earning(self, event):
        reply_token = event.reply_token
        message = template.enter_success
        total = 0
        for i in range(len(earn_list)) :
            if earn_list[i]['earn_type'] == earn_list[-1]['earn_type'] :
                total += int(earn_list[i]['earn_money'])
        message["body"]["contents"][0]["text"] = "已在 " + earn_list[-1]['earn_type'] + "類 加上   " + earn_list[-1]['earn_money'] + "元"
        message["body"]["contents"][1]["text"] = "本月 " + earn_list[-1]['earn_type'] + "類 已經累計 " + str(total) + "元"
        message_to_reply = FlexSendMessage("輸入成功！", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
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
        for i in range(len(spend_type)) :
            spend_list_tog[spend_type[i]] = 0
        for i in range(len(spend_list)) :
            spend_list_tog[spend_list[i]['spend_type']] += int(spend_list[i]['spend_money'])
        
        labels = []
        sizes = []
        for x, y in spend_list_tog.items():
            labels.append(x)
            sizes.append(y)
        plt.pie(sizes, labels=labels)
        plt.axis('equal')
        plt.show()
        plt.savefig('chart.png', dpi=300)
        '''
        CLIENT_ID = "fe5468cf1e4d868"
        PATH = "chart.png"
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(PATH, title="upload")
        print(uploaded_image.link)
        
        plt.figure(figsize=(6,9))    # 顯示圖框架大小
        separeted = (0, 0, 0.3, 0, 0.3)                  # 依據類別數量，分別設定要突出的區塊
        plt.pie(size,                           # 數值
                labels = labels,                # 標籤
                autopct = "%1.1f%%",            # 將數值百分比並留到小數點一位
                explode = separeted,            # 設定分隔的區塊位置
                pctdistance = 0.6,              # 數字距圓心的距離
                textprops = {"fontsize" : 12},  # 文字大小
                shadow=True)                    # 設定陰影
        plt.axis('equal')                                          # 使圓餅圖比例相等
        plt.title("Pie chart of car accident", {"fontsize" : 18})  # 設定標題及其文字大小
        plt.legend(loc = "best")                                   # 設定圖例及其位置為最佳
        plt.show()
        
        reply_token = event.reply_token
        message = message_template.introduction_message
        message_to_reply = FlexSendMessage("開啟圖表", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()
        '''

    def on_enter_watch_balance(self, event):
        reply_token = event.reply_token
        message = template.shiba_bar
        total_s = 0
        for i in range(len(spend_list)) :
            total_s += int(spend_list[i]['spend_money'])
        total_e = 0
        for i in range(len(earn_list)) :
            total_e += int(earn_list[i]['earn_money'])
        dif = total_e-total_s
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
        message = template.show_pic
        message_to_reply = FlexSendMessage("fsm diagram", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()