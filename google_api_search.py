#!bin/python3

# This Module is used to search via api created by you.

"""
num_of_results - resp["searchInformation"]["totalResults"]
search_time - resp["searchInformation"]["searchTime"]
link - resp["items"][index_value_in_loop]["link"]
title - resp["items"][index_value_in_loop]["title"]
about(expl.) - resp["items"][index_value_in_loop]["snippet"]

"""
import datetime

try:
	import requests
	import fake_useragent
	from urllib.parse import urlencode
	# import json
	from urllib3 import exceptions as urlexceptions

except ModuleNotFoundError:
	print("Required Modules Not Found")
	exit()
cx = "92079f4a8e99241f9"
api_key = "AIzaSyDNWaBv47hfsdk7-tRjBGZQjMNjF2VuWSI"

fk_obj = fake_useragent.FakeUserAgent()
user_agent = fk_obj.chrome


# noinspection PyTypeChecker
class GoogleApi:
	base_query = "https://www.googleapis.com/customsearch/v1"
	
	def __init__(self):
		self.query = ""
		self.headers = {"User-Agent": user_agent, "Connection": "keep-alive", }
		self.parameters = {"key": api_key, "cx": cx}
		self.session = requests.session()
		self.session.cookies.update(self.session.cookies)
		self.data = """"""
	
	def search(self, query):
		self.parameters['q'] = query
		try:
			resp = self.session.get(GoogleApi.base_query, headers=self.headers,
									params=self.parameters, allow_redirects=True)
			
			# self.query = GoogleApi.base_query+urllib.parse.urlencode(self.parameters)+self.query
			# resp = self.session.get(self.query)
			# print(resp.url, resp.status_code, sep="\t")
			print(resp.url)
			self.data = resp.json()
			return GoogleApi.parseJSONData(self)
		
		except urlexceptions:
			with open("error,log", 'a', encoding="utf-8") as F:
				F.write("500 - INTERNAL ERROR - ERROR IN THE CODE" + datetime.datetime.now() + '\n')
			return [500, ["ERROR_CODE : INTERNAL ERROR", "There is an Error in the URL or Search-Engine."]]
		
		except TypeError:
			print("A Type Error")
	
	def parseJSONData(self):
		json_data = self.data
		result = ""
		try:
			# noinspection PyTypeChecker
			num_of_results = json_data["searchInformation"]["totalResults"]
			search_time = json_data["searchInformation"]["searchTime"]
			data_of_each_website = []
			print(num_of_results, search_time, sep='\n')
			if int(num_of_results) == 0:
				result = [200,["OK", search_time, []]]
			
			if int(num_of_results) > 0:
				for each_url in json_data["items"]:
					# print(each_url)
					link = each_url["link"]
					title = each_url["title"]
					try:
						about = each_url["snippet"]
					except KeyError:
						about = "No Data to Show. Please Visit Website"
					data_of_each_website.append(title + '\n' + link + '\n' + about)
				# print(title, about, link, sep='\n')
				result = [200, ["OK", search_time, data_of_each_website]]
		
		except KeyError:
			error_code = json_data["error"]["code"]
			error_message = json_data["error"]["message"]
			error_status = json_data["error"]["status"]
			result = [error_code, [error_status, error_message]]
		
		finally:
			return result


# https://cse.google.com/cse?cx=92079f4a8e99241f9#gsc.tab=0&gsc.q=Hi
# https://www.googleapis.com/customsearch/v1?key=AIzaSyDNWaBv47hfsdk7-tRjBGZQjMNjF2VuWSI&cx=92079f4a8e99241f9&q=lectures
# https://www.googleapis.com/customsearch/v1?key=AIzaSyDNWaBv47hfsdk7-tRjBGZQjMNjF2VuWSI&q=Hi&cx=92079f4a8e99241f9

try:
	g1 = GoogleApi()
	# print(g1.search("Chandrayaan3"))

except Exception as E:
	print("Modules Not Found.")
