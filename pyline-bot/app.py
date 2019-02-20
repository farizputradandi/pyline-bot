from __future__ import unicode_literals

import errno,requests, json
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

app = Flask(__name__)

line_bot_api = LineBotApi('UaF2D7W5UZLstQUdBJyztahkil9/syi0gr0Eg6Sq5E0IuYy2+YKcMYbtMjFkoppwYk61szUAXEgbKfc053tod/nLchouY/IX3CDTwDTj7mlKWa+DkZ+u9lKOL960RH3VL2CUBVc1tqge7Wbv4OLejgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e2eb2183b117b019c8840b7754411b85')

#function
def getJadwalSholat(namakota):

    URL = "https://time.siswadi.com/pray/" + namakota
    getrequest = requests.get(URL)
    jsonnya = getrequest.json()

    subuh = jsonnya['data']['Fajr']
    dzuhur = jsonnya['data']['Dhuhr']
    ashar = jsonnya['data']['Asr']
    magrhib = jsonnya['data']['Sunset']
    isya = jsonnya['data']['Isha']
 
    output ="Jadwal Sholat hari ini di kota " + namakota + " adalah" + "\n" + "Subuh : " + subuh + "\n" "Dzuhur : " + dzuhur + "\n" "Ashar : " + ashar + "\n" "magrhib : " + magrhib + "\n" "Isya : " + isya + "\n"

    return (output)

def getQuotes(namakota):
    URL = "https://favqs.com/api/qotd" 
    getrequest = requests.get(URL)
    jsonnya = getrequest.json()
    quotenya = jsonnya['quote']['body']  
    output = quotenya +" (FPD)"  
    return (output)

    
def lala():
    return ("masuk ke fungsi yes")

@app.route("/callback", methods=['POST'])
def callback():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """ Here's all the messages will be handled and processed by the program """

    msg = (event.message.text).lower()

#split text input
    StrMsg=msg.split(' '); #input = jadwal bandung

#bout text

    if 'hello' in msg:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=['Hello, world 1', 'Hello, world 2'])) 
 
    elif 'hola' in msg:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="hello pengguna")) 

    elif 'kirim stiker' in msg:
        line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(  package_id='1',
            sticker_id='1')) 
 

    elif 'kirim map' in msg:
        line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
    title='my location',
    address='Tokyo',
    latitude=35.65910807942215,
    longitude=139.70372892916203))
 


#bout tools
    elif msg == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='invit aku lagi dong :('))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='invit aku lagi dong :('))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="yes gabisa kick aku"))

#bout api
    elif 'sholat' in StrMsg[0]: 
        namakota = StrMsg[1]
        hasil = getJadwalSholat(namakota) 


        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=hasil))


    elif 'qotd' in msg:    
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=getQuotes("qotd")))

#bout profile
    elif 'hai min' in msg:    
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Hi "+profile.display_name+" :P"))

    elif 'list member' in msg:    
        profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=profile.display_name))
    
 
#bout button
    elif 'confirm' in msg:
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageAction(label='Yes', text = lala()), #masuk kefungsi lala
            MessageAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage( #buat nampilin label diatas
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    

#this require handler postback event yg bagian postbackaction
    elif 'buttons' in msg:
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping'),
                # PostbackAction(label='datetime', data='datetime_postback'),
                # PostbackAction(label='date', data='date_postback'),
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
  

    # else:    
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text=event.message.text))

@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message( 
            event.reply_token, TextSendMessage(text=event.postback.params['datetime'])) 
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='hai felas ')) # + event.source.type //jenis nya grup atau multichat


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("babay felas")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
