from dataclasses import dataclass, field


@dataclass
class SlackBot:
    id: str
    url: str
    signing_secret: str
    to_proxy_token: str
    to_bot_token: str

    conversations: dict = field(default_factory=dict)

    def add_conversation(self, conversation_id: str, token: str):
        self.conversations[conversation_id] = token
