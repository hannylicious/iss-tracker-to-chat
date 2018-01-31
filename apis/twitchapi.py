# twitchapi.py
from apis.twitchcredentials import TwitchCredentials
import socket
import time
import re

class TwitchApi(object):
	def __init__(self):
		RATE = (20/30) # Messages per second
		CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
		TIMEOUT_PAT = [
		    r"dumbass",
		    r"some_pattern"
		    ]

	def chat(sock, msg):
		"""
		Sends a chat msg to the server.
		Keyword arguments
		sock -- socket to send the msg
		msg -- the message to be sent
		"""
		sock.send(("PRIVMSG {} :{}\r\n".format(TwitchCredentials.CHAN, msg)).encode("UTF-8"))

	def ban(sock, user):
	    """
	    ban a user from current channel
	    keyword arguments:
	    sock -- socket
	    user -- user to banx
	    """
	    chat(sock, ".ban {}".format(user))

	def timeout(sock, user, secs=600):
	    """
	    Time a user out for set time
	    sock -- socket
	    user -- user to be timed out
	    secs -- the length of timeout (default 600)
	    """
	    chat(sock, ".timeout {}".format(user,secs))

	# Network functions
	def connect():
		sock = socket.socket()
		sock.connect((TwitchCredentials.HOST, TwitchCredentials.PORT))
		sock.send("PASS {}\r\n".format(TwitchCredentials.PASS).encode("utf-8"))
		sock.send("NICK {}\r\n".format(TwitchCredentials.NICK).encode("utf-8"))
		sock.send("JOIN {}\r\n".format(TwitchCredentials.CHAN).encode("utf-8"))
		return sock

	def bot_loop():
	    while connected:
	        response = s.recv(1024).decode("utf-8")
	        if response == "PING :tmi.twitch.tv\r\n":
	            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
	        else:
	            username = re.search(r"\w+", response).group(0)
	            message = CHAT_MSG.sub("", response)
	            #print(message)
	            print(username + ": " +message)
	            for pattern in TIMEOUT_PAT:
	                if re.match(pattern, message):
	                    timeout(s, username, 10)
	                    break
	        time.sleep(1 / RATE)
