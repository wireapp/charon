from dataclasses import dataclass


@dataclass
class Config:
    roman_url: str
    signing_secret: str

    bot_url: str
