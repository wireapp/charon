# Charon
[![GitHub version](https://badge.fury.io/gh/wireapp%2Fcharon.svg)](https://badge.fury.io/gh/wireapp%2Fcharon)
![CI/CD](https://github.com/wireapp/charon/workflows/CI/CD/badge.svg)
![Release Pipeline](https://github.com/wireapp/charon/workflows/Release%20Pipeline/badge.svg)

## Bridge between Slack and Wire
Charon is proxy converting Slack Bot API calls to Wire (using [Roman](https://github.com/dkovacevic/roman)) and back
and thus allows to use subset of Slack Bots in the Wire. 

Please note that this is simple proof of concept work, that was developed in few days just to prove that it is possible
to use existing Slack Bot and connect it to the [Wire](https://wire.com) API.
The code looks accordingly.

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

## Slack bot onboarding
To add new Slack bot instance to Charon one must register the bot in the Roman and in the Charon.
Both services have Swagger API for registration process or one can use CLI 
from the [repository with example](https://github.com/LukasForst/slack-onboarding-bot/tree/master/cli). 

## Example
Example bot with complete CLI and description can be found [here](https://github.com/LukasForst/slack-onboarding-bot).
It is based on the official [tutorial](https://github.com/slackapi/python-slackclient/tree/master/tutorial),
where we changed just the backend URL (from Slack to Charon).
In that repo, there's also CLI, which allows to run the bot targeting Slacks API or Wire with single command.
```bash
make run-wire
```
To target Wire or to target Slack:
```
make run-slack
```

## Known issues 
This is just a PoC project, to show that it is indeed possible to partially map Slack API 
and to use Slack bots in the Wire infrastructure. 
However, there are some limitations and therefore mapping between API can't be 1:1.

Known limitations so far:
* Wire does not have concept of Slack's `channel`
    * channels are in Slack public and all bots can read from them even though they are not part of that channel,
    Wire does not have concept of public channels as public channels couldn't be encrypted
    * Charon therefore maps `channel` to `group`, where group is Slack's concept of private conversations
* Wire does not support commands
    * Slack has special type of the message which is called `command` that is basically `/do something`
    * This can be implemented in Charon in the future by simply parsing incoming message from the Roman
    and if it starts with `/`, Charon would transform that into the `command` message.
* Bot can not initiate conversation
    * In the Slack, bot can create conversation with anyone, 
    Wire does not allow conversations initiated by bot for security reasons.
* Various events
    * Wire does not support messages pins yet
    * Wire has only hearth reaction, so no other emojis can be used for reactions.
    * In general, vast majority of events from Slack are not, or even couldn't be, mapped to Wire events
    as Wire tries to limit the API and events because of security.
    However, that shouldn't be problem in the future, because bot should react only to events that we want it to react,
    therefore we are able to simulate almost anything. 

There are, for sure, more limitation then those listed here, but we haven't found out yet.

## Running Charon
Charon needs following configuration - `ROMAN_URL`, `REDIS_URL`, `REDIS_PORT`.
To run Charon locally, please create file `config.py` which contains following runtime variables:
```python
ROMAN_URL = 'http://proxy.services.zinfra.io'

REDIS_URL = 'localhost'
REDIS_PORT = '6379'
```
and spin the Redis instance - there's one in the docker-compose.

To run Charon inside docker-compose, just execute `docker-compose up`.

## Docker Images
Charon has public [docker image](https://hub.docker.com/r/lukaswire/charon).
```bash
lukaswire/charon
```
Tag `latest` is current master branch - each commit is build and tagged as `latest`.
[Releases](https://github.com/wireapp/charon/releases) have then images with corresponding tag.

## Development
It uses `pipenv` for dependencies management. 
Currently build on top of:
- [Flask](https://github.com/pallets/flask) - server
- [flask-restx](https://github.com/python-restx/flask-restx) - requests processing, swagger
- [requests](https://github.com/psf/requests) - sending HTTP requests to Roman/Bot
- [emoji](https://github.com/carpedm20/emoji/) - emoji processing (from Slack to Wire)
- [redis](https://github.com/andymccurdy/redis-py) - storage for information about bots and services
- [dacite](https://github.com/konradhalas/dacite) - simple Dataclass parsing from JSON

## Releases
See [releases page](https://github.com/wireapp/charon/releases) for more info.

In `0.0.2` we added support for the blocks, emojis 
and run the official welcome slack bot from the [tutorial](https://github.com/slackapi/python-slackclient/tree/master/tutorial)
through the proxy.
![alt text](resources/welcome_bot-wire.png "Working example of the proxy.")
