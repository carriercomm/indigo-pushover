#! /usr/bin/env python
# -*- coding: utf-8 -*-

####################
# Pushover plugin for Indigo 6
#
# Based on the work of Chad Francis (http://www.thechad.io)
# Further Developed by Marcel Trapman and others.
####################

import httplib, urllib, sys, os


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

    ########################################
    # actions
    ########################################
    def send(self, pluginAction):
        parameters = {}

        try:
            token = self.pluginPrefs["applicationapikey"]

            if "pushtoken" in pluginAction.props and pluginAction.props["pushtoken"]:
                token = pluginAction.props["pushtoken"]

            if not token:
                raise Exception

            # Mandatory
            parameters["token"] = token
        except:
            indigo.server.log(u"Mandatory token not set (correct)", isError = True)

            return

        try:
            user = self.pluginPrefs["userkey"]

            if not user:
                raise Exception

            # Mandatory
            parameters["user"] = user
        except:
            indigo.server.log(u"Mandatory user not set", isError = True)

            return

        try:
            message = u"%s" % pluginAction.props["txtmessage"]

            while "%%v:" in message:
                message = self.substituteVariable(message)

            # Mandatory
            parameters["message"] = message
        except:
            indigo.server.log(u"Mandatory message not set", isError = True)

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
            parameters["sourd"] = pluginAction.props["pushsound"]

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
                            indigo.server.log(u"Mandatory Emergency retries not set (correct)", isError = True)

                            return

                        try:
                            expire = self.integerValue(pluginAction.props["expire"])

                            if expire > 86400:
                                expire = 86400

                            # Mandatory when Emergency Priority is set
                            parameters["expire"] = expire
                        except:
                            indigo.server.log(u"Mandatory Emergency expiry not set (correct)", isError = True)

                            return

                        if "callback" in pluginAction.props and pluginAction.props["callback"]:
                            # Optional when Emergency Priority is set
                            parameters["callback"] = self.integerValue(pluginAction.props["callback"])
            except:
                indigo.server.log(u"Priority is not set (correct)", isError = True)

                return

        conn = httplib.HTTPSConnection("api.pushover.net:443")
        conn.request(
            "POST",
            "/1/messages",
            urllib.urlencode( parameters ),
            {"Content-type": "application/x-www-form-urlencoded"})

    ########################################
    # Helper methods
    ########################################
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

        return None
