from rasa_nlu.model import Interpreter
import json
from flask import Flask,request
from pymessenger.bot import Bot
import requests


app=Flask(__name__)
#Initializing RASA interpreter 
interpreter = Interpreter.load("./models/current/nlu")

ACESS_TOKEN='EAAF7Cy0kEX4BACS9krGlqO6OZBFxEG8u98nKZA1n0eTOdHjss6mFqHnB62GPhJLW1kUck8Q0I9RIyVJkSr1UhPWDZBxVPCQ40DaTKTimhY7uHU6xJBtjy5vfZBWbX8et1hoZAHe69gFku5NVNbJBhoZCuvE8aPD0XVhS8G85wZBDR1ZCAcxfUUi3'
VERIFY_TOKEN='lmnverify'

bot=Bot(ACESS_TOKEN)

def get_intent(response):
	if response.get('intent'):
		return response['intent']['name']

	return ''

def get_entity(response,entity):
	if response.get('entities'):
		entity_value=[i['value'] for i in response['entities'] if i['entity'] == entity]
		if len(entity_value) > 0:
			return entity_value[0]
		return ''

def restaurant_search (response):
	location=get_entity(response,'location')
	cuisine=get_entity(response,'cuisine')

@app.route('/',methods=['GET','POST'])
def webhook():
	if request.method == 'GET':
		if request.args.get('hub.verify_token')== VERIFY_TOKEN:
			return request.args.get('hub.challenge')
		return 'Invalid Token'
	else:
		print('else')
		data=request.get_json()
		if data['object'] == 'page':
			for event in data['entry']:
				messaging = event['messaging']
				for message in messaging:
					recipient_id=message['sender']['id']
					if message['message'].get('text'):
						text= message['message']['text']
						print('texrt')
						response=interpreter.parse(text)
						print(response)
						if get_intent(response) == 'greet' : 
							bot.send_text_message(recipient_id,text)
						
						elif get_intent(response) == 'restaurant_search' : 
							bot.send_text_message(recipient_id,"So you wanna eat?")
							location_entity=get_entity(response,'location')
							if location_entity is not None :
								print(location_entity)
								bot.send_text_message(recipient_id,"Let me check if i can find a place near {}".format(location_entity))
							cuisine_entity=get_entity(response,'location')
							if cuisine_entity is not None:
								print(cuisine_entity)
								bot.send_text_message(recipient_id,"I will look for a good place which serves good {} food".format(cuisine_entity))
							bot.send_text_message(recipient_id,"Right?")
						elif get_intent(response) == 'thankyou':
							bot.send_text_message(recipient_id,'Welcome, Glad to help you.Tc')

						else:
							#tex2='Did you just send \'{} \''.format(text)
							bot.send_text_message(recipient_id,('Did you just send '+str(text)))
							#bot.send_text_message(recipient_id,"I think the intent of oyur previous message is : " + response['intent']['name'])


	return 'OK'

app.run(port=5000,debug=True)

'''message = "I am looking for a restaurant in chennai food"
result = interpreter.parse(message)
print(json.dumps(result,indent=2))'''