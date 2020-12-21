import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

load_dotenv()

machine = TocMachine(
    states=["user", "mainmenu", "introduction", "keep_accounts", "spending_mode", "earning_mode", "watch_all_record", "enter_spending", "enter_earning", "edit", "edit_data", "watch_chart", "watch_balance", "watch_video", "show_fsm"],
    transitions=[
        {"trigger": "advance", "source": "user", "dest": "mainmenu", "conditions": "is_going_to_mainmenu"},
        {"trigger": "advance", "source": "mainmenu", "dest": "mainmenu", "conditions": "is_going_to_mainmenu"},
        {"trigger": "advance", "source": "mainmenu", "dest": "introduction", "conditions": "is_going_to_introduction"},
        {"trigger": "advance", "source": "mainmenu", "dest": "keep_accounts", "conditions": "is_going_to_keep_accounts"},
        {"trigger": "advance", "source": "mainmenu", "dest": "watch_chart", "conditions": "is_going_to_watch_chart"},
        {"trigger": "advance", "source": "mainmenu", "dest": "watch_balance", "conditions": "is_going_to_watch_balance"},
        {"trigger": "advance", "source": "mainmenu", "dest": "watch_video", "conditions": "is_going_to_watch_video"},
        {"trigger": "advance", "source": "mainmenu", "dest": "show_fsm", "conditions": "is_going_to_show_fsm"},
        {"trigger": "advance", "source": "keep_accounts", "dest": "spending_mode", "conditions": "is_going_to_spending_mode"},
        {"trigger": "advance", "source": "keep_accounts", "dest": "earning_mode", "conditions": "is_going_to_earning_mode"},
        {"trigger": "advance", "source": "keep_accounts", "dest": "watch_all_record", "conditions": "is_going_to_watch_all_record"},
        {"trigger": "advance", "source": "spending_mode", "dest": "enter_spending", "conditions": "is_going_to_enter_spending"},
        {"trigger": "advance", "source": "earning_mode", "dest": "enter_earning", "conditions": "is_going_to_enter_earning"},
        {"trigger": "advance", "source": ["enter_spending", "enter_earning"], "dest": "mainmenu", "conditions": "is_going_to_mainmenu"},
        {"trigger": "advance", "source": "enter_spending", "dest": "edit", "conditions": "is_going_to_edit"},
        {"trigger": "advance", "source": "enter_earning", "dest": "edit", "conditions": "is_going_to_edit"},
        {"trigger": "advance", "source": "edit", "dest": "edit_data", "conditions": "is_going_to_edit_data"},
        {"trigger": "go_back", "source": ["introduction", "keep_accounts" , "watch_all_record", "enter_spending", "enter_earning", "edit", "edit_data", "watch_chart", "watch_balance", "watch_video", "show_fsm"], "dest": "user"},
        #{"trigger": "go_back", "source": ["enter_spending", "enter_earning"], "dest": "keep_accounts"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")
    return "OK"

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")

    #user_id = event.source.user_id
    #print("user_id =", user_id)
    
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")    

if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    #machine.get_graph().draw("fsm.png", prog="dot", format="png")
    app.run(host="0.0.0.0", port=port, debug=True)
