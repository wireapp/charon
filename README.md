# Charon
## The bridge between Slack and Wire

Charon is proxy converting Slack Bot API calls to Wire (using [Roman](https://github.com/dkovacevic/roman)) and back.

Please note that this is simple proof of concept work, that was developed in few days just to prove that it is possible
to use existing Slack Bot and connect it to the [Wire](https://wire.com) API.
The code looks accordingly.

## Development

It uses `pipenv` for dependencies management. 
Currently build on top of:
- [Flask](https://github.com/pallets/flask)
- [flask-restx](https://github.com/python-restx/flask-restx)
- [requests](https://github.com/psf/requests)

## Running the proxy
Please create file `config.py` which contains following runtime variables:
```python
ROMAN_URL = '<Roman URL>'
```

## How does Charon work
It exposes Slack-like API which is called by the Slack Bot.
Then it transforms the API call to one that can be processed by [Roman](https://github.com/dkovacevic/roman).
The very same thing happens when new message is received from the Roman,
the message is transformed (some information are missing in the default calls from the Roman, so the proxy ask for them)
 to the Slack version of message and sent to the Slack Bot API.
 
 > Is it slow?
 
 Not really, it is slower than running native [Lithium](https://github.com/wireapp/lithium),
 but when I was testing raw Slack Bot with Slack API, the response time was between 1.4 and 2.5 seconds.
 The setup with Charon and Roman had response times around 1.2 and 2.5 seconds, so no leg basically. 

## Using the proxy
1) register Slack Bot in the register endpoint, please note that `to_bot_token` is token provided by Roman.
2) change bot's base URL to target this service `/slack`

## Missing 
Almost everything... this is just a PoC project which was tested only on Echo Bot,
which sends everything back.
But it works!

### Version 0.0.1
We developed echo bot based on the [Slack tutorial](https://github.com/slackapi/python-slackclient/tree/master/tutorial)
and run it through the Charon.

![alt text](resources/working_example.png "Working example of the proxy.")

### Version 0.0.2
We added support for the blocks, emojis and run the official welcome slack bot from the [tutorial](https://github.com/slackapi/python-slackclient/tree/master/tutorial)
through the proxy.
![alt text](resources/welcome_bot-wire.png "Working example of the proxy.")
