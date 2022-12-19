import os


class TwitchCredentials(object):

    HOST = "irc.chat.twitch.tv"
    PORT = 6667
    NICK = os.environ.get("TWITCH_NICK")
    PASS = os.environ.get("TWITCH_OAUTH")
    CHAN = "#" + str(os.environ.get("TWITCH_CHANNEL"))
