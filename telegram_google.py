#!bin/python3
# Google-Search using Telegram

import telebot
import google_api_search
import datetime

API_KEY = "YOUR_API_KEY"
user_list = []
feedbacK_list = []
max_threads = 10
file_handlers = {}


def startup():
	global user_list
	global feedbacK_list
	global file_handlers
	with open("user_list.list", 'r', encoding="utf-8") as F:
		user_list = [int(i) for i in F]
	with open("feedback_list.list", 'r', encoding="utf-8") as F:
		feedbacK_list = [int(i) for i in F]
	feedback = open("feedback.data", 'a', encoding="utf-8")
	donation = open("donation.data", 'a', encoding="utf-8")
	contact = open("contacts.list", 'a', encoding="utf-8")
	file_handlers["feedback"] = feedback
	file_handlers["donation"] = donation
	file_handlers["contact"] = contact


def conclude():
	global user_list
	global feedbacK_list
	user_list = [str(i) for i in user_list]
	feedbacK_list = [str(i) for i in feedbacK_list]
	with open("user_list.list", 'w', encoding="utf-8") as F:
		F.write('\n'.join(user_list))
	with open("feedback_list.list", 'w', encoding="utf-8") as F:
		F.write('\n'.join(feedbacK_list))
	for _ in file_handlers:
		file_handler = file_handlers[_]
		file_handler.close()
	
	print("Exit Complete...")


# noinspection PyMethodMayBeStatic
class Google_Telegram:
	API_KEY = "0" * 12
	global user_list
	
	def __init__(self, api_key):
		print("Initializing...")
		Google_Telegram.API_KEY = api_key
		startup()
		self.bot = telebot.TeleBot(Google_Telegram.API_KEY)
		Google_Telegram.botHandler(self)
		Google_Telegram.setHandlers(self)
		self.engine = google_api_search.GoogleApi()
		Google_Telegram.message_handlers(self)
	
	def botHandler(self):
		@self.bot.message_handler(commands=["stop0907"])
		def adminCommands(message):
			print(message.from_user.id, message.from_user.username)
			self.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
			if message.from_user.id == 5662129294:
				self.bot.send_message(chat_id="5662129294", text=f"Mr. Admin,\n  The Bot is being Stopped via Remote "
																 f"Messaging.\n If Needed plese turn me ON.\n Details : \n Group Name : {message.chat.title}\n"
																 f"Group ID : {message.chat.id}")
				# Delete the Message
				self.bot.stop_bot()
		
		print("Admin Section...  Ready")
	
	def setHandlers(self):
		# Add JOin Request
		self.bot.add_chat_join_request_handler(Google_Telegram.checkStatus)
		self.bot.allow_sending_without_reply = True
		print("Handler Section...  Ready")
	
	def checkStatus(self, update):
		message = update.message
		if message.from_user.is_bot is False:  # He is a USer
			Google_Telegram.new_member_joined(self, message.chat.id, message.from_user.id, message.from_user.username)
			self.bot.approve_chat_join_request(chat_id=message.chat.id, user_id=message.from_user.id)
		else:
			with open("bots.data", 'a', encoding="utf-8") as F:
				F.write(message.from_user.id + '\n')
	
	def new_member_joined(self, chat_id, user_id, username):
		global user_list
		if chat_id == user_id:  # It is a Private ID
			pass  # Send start message
		
		self.bot.send_message(chat_id, f"Welcome {username}")
		user_list.append(user_id)
		print(chat_id, user_id, username)
	
	# noinspection PyUnresolvedReferences
	def message_handlers(self):
		global file_handlers
		
		@self.bot.message_handler(content_types=["audio", "animation", "video", "location", "file", "sticker", "image"])
		def otherMessages(message):
			if Google_Telegram.isPrivate(self, message):
				print(f"Recieved {message.content_type} on {message.chat.id} from {message.from_user.id}.")
				self.bot.reply_to(message,
								  f"Sorry! I don't understand {message.content_type} messages.\n Try sending me Messages.")
		
		@self.bot.message_handler(content_types=["contact"])
		def getContact(message):
			details = str(message.contact.phone_number) + ' '
			if message.contact.first_name is not None:
				details += message.contact.first_name + ' '
			if message.contact.user_id is not None:
				details += str(message.contact.user_id)
			
			details += '\n'
			file_handler = file_handlers["contact"]
			file_handler.write(details)
			print(f"Recieved Contact from {message.from_user.id}.")
			if Google_Telegram.isPrivate(self, message):
				self.bot.reply_to(message, "Recieved Contact.")
		
		@self.bot.message_handler(func=lambda msg: True)
		def MessageHandlerSeggregator(message):
			if message.chat.type == "private":
				privateMessageHandler(message)
			else:
				notCommand = filterGroupMessageCommands(
					message)  # Filter all the commands that a group user is trying to send
				if notCommand:
					# Check if it is a Converstion
					if isItSearch(message.text):
						message.text = message.text[1:]
						getMessage(message)
		
		def isItSearch(message):
			"""Check if it is a Message"""
			if message[0] == "?" and message != "?":
				# It is A Message
				return True
			return False
		
		def filterGroupMessageCommands(message):  # Delete Message such as Commands...
			chat_id = message.chat.id
			message_id = message.message_id
			text = message.text
			__cmds = text.split()
			if __cmds[0][0] == "/" and len(__cmds) == 1:
				self.bot.delete_message(chat_id=chat_id, message_id=message_id, timeout=5)
				return False
			return True
		
		def privateMessageHandler(message):
			global feedbacK_list
			command = message.text
			if command == "/feedback":
				feedbacK_list.append(message.from_user.id)
				self.bot.reply_to(message, "Help me by Giving Feedback")
			elif command == "/howtouse":
				self.bot.reply_to(message, "Search all your Queries in Google\n Example : Chandrayaan-3 ?")
				getMessage(message)
			elif command == "/help":
				self.bot.reply_to(message, """Directly Enter your Query as you would do in Google.\nIt is that Simple
						Index :
						/start - To Start this Bot.
						/help - For Any Help
						/howtouse - To see all its Function
						/feedback - Help us improve by giving Feedback
						""")
			elif command == "/donate":
				file_handler = file_handlers["donation"]
				file_handler.write(str(message.from_user.id) + "\n")
				self.bot.reply_to(message, "Thanks for the Kind Gesture.\n This is my Part-Time Work")
			
			elif command == "/start":
				username = message.from_user.username
				if username is None:
					self.bot.reply_to(message, f"Let's Get Started...")
				else:
					self.bot.reply_to(message, f"Hey {username}, Let's Get Started...")
			else:
				getMessage(message)
		
		def getMessage(message):
			global feedbacK_list
			global file_handlers
			print()
			user_id = message.from_user.id
			if user_id in feedbacK_list and message.chat.type == "private" and message.text != "/howtouse":
				feedbacK_list.remove(user_id)
				file_handler = file_handlers["feedback"]
				file_handler.write(message.text + " - " + str(user_id) + '\n')
				print("Feedback Recieved From - ", user_id)
				self.bot.send_animation(chat_id=message.chat.id,
										animation=open(r"thanks.gif", 'rb'))
			else:
				if message.text == "/howtouse":
					message.text = "Chandrayaan-3"
				temp_response = self.bot.send_animation(chat_id=message.chat.id,
														animation=open(r"loading.gif", 'rb'))
				msg = message.text
				print(message.from_user.id, " 's Query : ", msg)
				chat_id = message.chat.id
				message_id = temp_response.message_id
				a = self.engine.search(msg)
				print(a)
				status, func_info = a  # self.engine.search(msg)
				if status == 200:
					answer = "Time - " + str(round(func_info[1], 2)) + " seconds\n"
					# noinspection PySimplifyBooleanCheck
					if func_info[2] == []:
						answer += "No Results Found.\n Please Check Your Query."
					for __ in func_info[2]:
						answer += __
						answer += "\n\n"
				else:
					print("Failure")
					if status > 500:
						# Problem at the Server Side
						answer = "Looks Like an Server Issue..\nWait for Some Time :)"
					elif status > 400:
						# Problem at My Side.
						answer = "Unable To Fetch Your Query!\n Please Try Again Later :)"
						with open("Error400.log", 'a', encoding='utf-8') as fucked_up:
							fucked_up.write(status + ' - ' + func_info[0] + ' - ' + func_info[1] + ' - ' + str(
								datetime.datetime.now()) + '\n')
					else:
						# Unrecognized Error Occured
						with open("unrecognized_errors.log", 'a', encoding="utf-8") as fii:
							fii.write(status + ' - ' + func_info[0] + ' - ' + func_info[1] + ' - ' + str(
								datetime.datetime.now()) + '\n')
						answer = "Please verify your Query!"
				self.bot.delete_message(chat_id=chat_id, message_id=message_id)
				self.bot.send_message(message.chat.id, answer)
				print("MEssage ID : " + str(message.chat.id) + " COmplete.")
	
	def isPrivate(self, message):
		if message.chat.type == "private":
			return True
		return False


try:
	if __name__ == "__main__":
		startup()
		g1 = Google_Telegram(API_KEY)
		# g1.bot.set_my_short_description(short_description=r"Google-Search 🤖 ")
		# g1.bot.set_my_description("This Bot is Still Under-Development!")
		g1.bot.infinity_polling(long_polling_timeout=15)


except KeyboardInterrupt:
	print("Stopping...")

except Exception as e:
	print("Error ", e)

finally:
	conclude()
