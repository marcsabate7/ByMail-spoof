from socket import *
import time
import ssl
import base64
from io import StringIO

class SendMail(object):
	def __init__(self):
		self.mail_server =""
		self.rcpt_to = ""
		self.email_data = ""
		self.helo = ""
		self.mail_from = ""
		self.starttls = False
		self.verbose = False

		self.client_socket = None
		self.tls_socket = None
	
	def set_mail_info(self, mail_server, rcpt_to, email_data, helo, mail_from, starttls=False, verbose=False):
		self.mail_server = mail_server
		self.rcpt_to = rcpt_to
		self.email_data = email_data
		self.helo = helo
		self.mail_from = mail_from
		self.starttls = starttls
		self.verbose = verbose


	def send_email(self):
		self.establish_socket()
		try:
			if self.starttls == True:
				self.send_smtp_cmds(self.tls_socket)
				self.send_quit_cmd(self.tls_socket)
			else:
				self.send_smtp_cmds(self.client_socket)
				self.send_quit_cmd(self.client_socket)
			self.close_socket()
		except Exception as e:
			import traceback
			traceback.print_exc()	

	def __del__(self):
		self.close_socket()