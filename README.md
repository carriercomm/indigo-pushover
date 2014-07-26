indigo-pushover
===============

[Indigo](http://www.perceptiveautomation.com/indigo/index.html) plugin  - send push notifications to mobile devices via [Pushover](http://www.pushover.net).

### Requirements

1. [Indigo 6](http://www.perceptiveautomation.com/indigo/index.html) or later (pro version only)
2. Valid Pushover [API key](https://pushover.net/api)
3. Valid Pushover [user key](https://pushover.net/faq#overview-what)

### Installation instructions release version
1. Download latest release [here](https://github.com/discgolfer1138/indigo-pushover/releases)
2. Follow [standard plugin installation process](http://bit.ly/1e1Vc7b)

### Installation instruction repository version
When you decide to download the plugin you will download a zipped archive named 'indigo-mysensors-master.zip'.
Unzip the archive and rename the folder to 'MySensors.indigoPlugin'.

When you have Indigo installed the folder will show as a single file (a so called package).
When you doubleclick on the file you will automatically open Indigo (or bring it to the front) and you will be asked if you want to install and enable it.

### Actions Supported
* Send Push Notification

### Important
Please check out the api documentation from Pushover when you want to know about the details but this is what was implemented:

[Mandatory] configuration menu
token - your application's API token (it is advised to set a default one to use here)
user - the user/group key (not e-mail address), viewable when logged into our dashboard

[Mandatory] trigger/action group
token - your application's API token (when not set in the configuration menu it mandatory here)
message - your message

[Optional] trigger/action group
token - your application's API token (when set in the configuration menu it is optional here)
device - your user's device name to send the message directly to that device, rather than all of the user's devices
title - your message's title, otherwise your app's name is used
url - a supplementary URL to show with your message
url title - a title for your supplementary URL, otherwise just the URL is shown
priority - send as -2 to generate no notification/alert, -1 to always send as a quiet notification, 1 to display as high-priority and bypass the user's quiet hours, or 2 to also require confirmation from the user

[When Emergency-priority is set]
interval - the number of seconds between retries (minimum is 30 seconds, mandatory)
expiry - the number of seconds after which you are not asked for confirmation anymore (maximum is 86400 seconds,mandatory)
callback - publicly-accessible URL to which the confirmation will be sent (optional)


