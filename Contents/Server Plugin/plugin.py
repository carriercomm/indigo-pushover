#! /usr/bin/env python
# -*- coding: utf-8 -*-

####################
# Pushover plugin for Indigo 6
#
# Based on the work of Chad Francis (http://www.thechad.io)
# Further Developed by Marcel Trapman and others.
####################

import httplib, urllib, indigo, re

class Plugin(indigo.PluginBase):

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

		self.debug = True

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")


	#### validation

	def validatePrefsConfigUi(self, valuesDict):

		errorsDict = indigo.Dict()

		## validate app key
		appKeys = valuesDict["appKeys"]

		if not appKeys:
			errorsDict["appKeys"] = "Please enter at least one key"
		if len(appKeys) < 30:
			errorsDict["appKeys"] = "key must be at least 30 characters"

		## validate user key length
		userKey = valuesDict["userKey"]

		if not userKey:
			errorsDict["userKey"] = "Please enter your user key"

		if len(userKey) <> 30:
			errorsDict["userKey"] = "key must be 30 characters"

		## validate user key with Pushover
		if appKeys and len(appKeys) >= 30 and userKey and len(userKey) == 30:
			parameters = {
				"token": appKeys,
				"user": userKey
			}
			conn = httplib.HTTPSConnection("api.pushover.net:443")
			conn.request(
				"POST",
				"/1/users/validate.json",
				urllib.urlencode( parameters ),
				{"Content-type": "application/x-www-form-urlencoded"})
			resp = conn.getresponse()

			if resp.status <> 200:
				import simplejson as json
				jsonData = json.loads(resp.read())
				if "token" in jsonData:
					errorsDict["appKeys"] = "app key not valid, visit pushover.net to verify"
				elif "user" in jsonData:
					errorsDict["userKey"] = "user key not valid, visit pushover.net to verify"
				else:
					errorsDict["showAlertText"] = "An error occurred while checking your validation your keys with Pushover, please try again later"

		## check if any errors were encountered
		if len(errorsDict) > 0:
			return (False, valuesDict, errorsDict)

		return (True, valuesDict)

	#### actions

	def sendPushNotification(self, pluginAction):
		parameters = {}

		try:
			token = self.pluginPrefs["applicationApiKeys"]

			if "pushtoken" in pluginAction.props and pluginAction.props["pushtoken"]:
				token = pluginAction.props["pushtoken"]

			if not token:
				raise Exception

			# Mandatory
			parameters["token"] = token
		except:
			self.errorLog(u"Mandatory token not set (correct)")

			return

		try:
			user = self.pluginPrefs["userkey"]

			if not user:
				raise Exception

			# Mandatory
			parameters["user"] = user
		except:
			self.errorLog(u"Mandatory user not set")

			return

		try:
			message = u"%s" % pluginAction.props["txtmessage"]

			while "%%v:" in message:
				message = self.substituteVariable(message)

			# Mandatory
			parameters["message"] = message
		except:
			self.errorLog(u"Mandatory message not set")

			return

		if "txttitle" in pluginAction.props and pluginAction.props["txttitle"]:
			title = u"%s" % pluginAction.props["txttitle"]

			while "%%v:" in title:
				title = self.substituteVariable(title)

			# Optional
			parameters["title"] = title

		if "pushdevice" in pluginAction.props and pluginAction.props["pushdevice"]:
			# Optional
			parameters["device"] = pluginAction.props["pushdevice"]

		if "pushsound" in pluginAction.props and pluginAction.props["pushsound"]:
			# Optional
			parameters["sound"] = pluginAction.props["pushsound"]

		if "pushurl" in pluginAction.props and pluginAction.props["pushurl"]:
			# Optional
			parameters["url"] = pluginAction.props["pushurl"]

		if "pushurltitle" in pluginAction.props and pluginAction.props["pushurltitle"]:
			# Optional
			parameters["url_title"] = pluginAction.props["pushurltitle"]

		if "priority" in pluginAction.props and pluginAction.props["priority"]:
			try:
				# Optional
				priority = self.integerValue(pluginAction.props["priority"])

				if 0 <> priority:
					parameters["priority"] = priority

					if priority == 2:
						try:
							retries = self.integerValue(pluginAction.props["retry"])

							if retries < 30:
								retries = 30

							# Mandatory when Emergency Priority is set
							parameters["retry"] = retries
						except:
							self.errorLog(u"Mandatory Emergency retries not set (correct)")

							return

						try:
							expire = self.integerValue(pluginAction.props["expire"])

							if expire > 86400:
								expire = 86400

							# Mandatory when Emergency Priority is set
							parameters["expire"] = expire
						except:
							self.errorLog(u"Mandatory Emergency expiry not set (correct)")

							return

						if "callback" in pluginAction.props and pluginAction.props["callback"]:
							# Optional when Emergency Priority is set
							parameters["callback"] = self.integerValue(pluginAction.props["callback"])
			except:
				self.errorLog(u"Priority is not set (correct)")

				return

		conn = httplib.HTTPSConnection("api.pushover.net:443")
		conn.request(
			"POST",
			"/1/messages",
			urllib.urlencode( parameters ),
			{"Content-type": "application/x-www-form-urlencoded"})
		conn.close()

	def generateTokenList(self, filter="", valuesDict=None, typeId="", targetId=0):
		tokens = self.pluginPrefs["applicationApiKeys"]
		tokens = tokens.replace(" ", "")

		tokenArray = tokens.split(",")
		tokenList = []

		for token in tokenArray:
			if ":" in token:
				name, key = token.split(":")
			else:
				name = token
				key = token

			tokenList.append((key, name))

		return tokenList

	#### Helper methods
	def integerValue(self, value):
		try:
			if isinstance(value, int):
				return int(value)
			elif isinstance(value, float):
				return int(float(value + 0.5))
			elif type(value) is bool:
				if value:
					return 1
				else:
					return 0
			elif type(value) is str:
				try:
					return int(value)
				except ValueError:
					return int(float(value + 0.5))
		except:
			pass

	def prepareTextValue(self, strInput):

		if strInput is None:
			return strInput
		else:
			strInput = strInput.strip()

			while "%%v:" in strInput:
				strInput = self.substituteVariable(strInput)

			#fix issue with special characters
			strInput = strInput.encode('utf8')

			return strInput

		return None
