from transitions.extensions import GraphMachine

from utils import send_text_message


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

    def is_going_to_watch_chart(self, event):
        text = event.message.text
        return text == "查看收支圖表"

    def is_going_to_watch_balance(self, event):
        text = event.message.text
        return text == "本月目前結餘"

    def on_enter_mainmenu(self, event):
        reply_token = event.reply_token
        message = message_template.main_menu
        message_to_reply = FlexSendMessage("開啟主選單", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)

    def on_enter_introduction(self, event):
        reply_token = event.reply_token
        message = message_template.introduction_message
        message_to_reply = FlexSendMessage("開啟功能介紹", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_keep_accounts(self, event):
        reply_token = event.reply_token
        message = message_template.introduction_message
        message_to_reply = FlexSendMessage("開啟記帳功能", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_watch_chart(self, event):
        reply_token = event.reply_token
        message = message_template.introduction_message
        message_to_reply = FlexSendMessage("開啟圖表", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()

    def on_enter_watch_balance(self, event):
        reply_token = event.reply_token
        message = message_template.introduction_message
        message_to_reply = FlexSendMessage("開啟結餘", message)
        line_bot_api = LineBotApi( os.getenv('LINE_CHANNEL_ACCESS_TOKEN') )
        line_bot_api.reply_message(reply_token, message_to_reply)
        self.go_back()
