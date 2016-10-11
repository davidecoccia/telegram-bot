import sys
import time
import telepot
import redis
import json
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton , KeyboardButton , ReplyKeyboardMarkup

r = redis.StrictRedis(host='192.168.99.100', port=6379, db=0)

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print(msg)
	print(msg.keys())
	print(msg.get('from').get('id'))
	print(msg['from']['first_name'])
	######persist the guy
	r.hset(msg.get('from').get('id'),'name',msg['from']['first_name'])
	print('Stored name: '+str(r.hget(msg.get('from').get('id'),'name')))
	print('Stored date: '+str(int(r.hget(msg.get('from').get('id'),'lastTalkedWith'))))
	#keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Press me', request_contact=True, request_location=True )],])
	######reply back to the guy
	if msg.get('contact') == None:
		bot.sendMessage(chat_id, 'Hi, '+str(r.hget(msg.get('from').get('id'),'name'))+' I know you! We last spoke on '+time.strftime("%Y/%m/%d %H:%M", time.localtime(
		int(r.hget(msg.get('from').get('id'),'lastTalkedWith'))
		)), reply_markup=keyboard)
	else:
		######persist the phone number
		r.hset(msg.get('from').get('id'),'phone_number',msg['contact']['phone_number'])
		bot.sendMessage(chat_id, 'Hey, '+str(r.hget(msg.get('from').get('id'),'name'))+' thanks for that.', reply_markup=keyboard)
	r.hset(msg.get('from').get('id'),'lastTalkedWith',msg['date'])

def on_callback_query(msg):
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
	print('Callback Query:', query_id, from_id, query_data)
	print(msg)
	bot.answerCallbackQuery(query_id, text='Got it')

TOKEN = '276922773:AAGeaw5SfOMPBd1-7peQKz5QJe9BpH39bEk'  # get token from command-line

bot = telepot.Bot(TOKEN)
#bot.sendMessage(264158450, 'Hi there! I need to know your phone number and location. Would you help me?')
keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='YAY! Share my number', request_contact=True, request_location=True )],[KeyboardButton(text='No Thanks' )]])
bot.message_loop({'chat': on_chat_message,
				  'callback_query': on_callback_query})
print('Listening ...')

while 1:
	time.sleep(10)