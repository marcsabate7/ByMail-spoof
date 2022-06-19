from http import client
from socket import *
import time
import ssl
import base64
from io import StringIO
import sys
from additional.common import *


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class SendMail(object):
	def __init__(self):
		self.mail_server =""
		self.rcpt_to = ""
		self.email_data = ""
		self.helo = ""
		self.mail_from = ""
		self.starttls = False
		self.verbose = False
		self.log = False
		self.num_thread = ""
		self.blocked_socket = False
		self.screen_report=[]

		self.client_socket = None
		self.tls_socket = None
	
	def set_mail_info(self, mail_server, rcpt_to, email_data, helo, mail_from, starttls=False, verbose=False,log = False,num_thread = 1):
		self.mail_server = mail_server
		self.rcpt_to = rcpt_to
		self.email_data = email_data
		self.helo = helo
		self.mail_from = mail_from
		self.starttls = starttls
		self.verbose = verbose
		self.log = log
		self.num_thread = num_thread


	def read_line(self, sock):
		buff = StringIO()
		while True:
			data = (sock.recv(1)).decode("utf-8")
			buff.write(data)
			if '\n' in data: break
		return buff.getvalue().splitlines()[0]


	def print_send_msg(self, msg):
		if self.verbose!=False:
			self.screen_report.append("<<< " + msg)
			#print("<<< " + msg)


	def print_recv_msg(self, client_socket):
		if self.verbose != False:
			prefix_msg = "\033[91m"+">>> "
			#print("\033[91m"+">>> ", end='')
		time.sleep(1)

		msg = ""
		while True:
			line  = self.read_line(client_socket)
			msg += line
			if self.verbose != False:
				if str("Service unavailable") in line:
					return "blocked"
				if str("Unfortunately") in line:
					return "blocked"
				#print(line) 
			if "-" not in line:
				break
			else:
				if len(line) > 5 and "-" not in line[:5]:
					break
			time.sleep(0.1)
		#if self.verbose != False:
			#print("\033[0m")
		
		self.screen_report.append(str(prefix_msg)+ str(msg))
		return msg



	def send_smtp_cmds(self, client_socket):
		dt_string = get_current_date()
		print("[Thread "+str(self.num_thread)+" - "+str(dt_string)+"]  " +color.YELLOW +"Sending ehlo..."+color.END)
		client_socket.send(b"ehlo "+self.helo+b"\r\n")
		time.sleep(0.1)
		self.print_send_msg("ehlo "+ self.helo.decode("utf-8")+"\r\n")
		self.print_recv_msg(client_socket)
		dt_string = get_current_date()
		print("[Thread "+str(self.num_thread)+" - "+str(dt_string)+"]  " +color.YELLOW +"Sending mail from..."+color.END)
		client_socket.send(b'mail from: '+self.mail_from+b'\r\n')
		time.sleep(0.1)
		self.print_send_msg('mail from: '+self.mail_from.decode("utf-8")+'\r\n')
		returned_message = self.print_recv_msg(client_socket)
		if returned_message == "blocked":
			dt_string = get_current_date()
			self.blocked_socket = True
			print("[Thread "+str(self.num_thread)+" - "+str(dt_string)+"]  " +color.RED +"Closing socket due to source IP blocked..."+color.END)
			self.close_socket()
		else:
			dt_string = get_current_date()
			print("[Thread "+str(self.num_thread)+" - "+str(dt_string)+"]  " +color.YELLOW +"Sending rcpt to..."+color.END)
			client_socket.send(b"rcpt to: "+self.rcpt_to+b"\r\n")
			time.sleep(0.1)
			self.print_send_msg("rcpt to: "+self.rcpt_to.decode("utf-8")+"\r\n")
			self.print_recv_msg(client_socket)
			dt_string = get_current_date()
			print("[Thread "+str(self.num_thread)+" - "+str(dt_string)+"]  " +color.YELLOW +"Sending data..."+color.END)
			client_socket.send(b"data\r\n")
			time.sleep(0.1)
			self.print_send_msg( "data\r\n")
			self.print_recv_msg(client_socket)
			
			client_socket.send(self.email_data+b"\r\n.\r\n")
			time.sleep(0.1)
			self.print_send_msg( self.email_data.decode("utf-8")+"\r\n.\r\n")
			self.print_recv_msg(client_socket)


	def send_quit_cmd(self, client_socket):
		if self.blocked_socket == False:
			client_socket.send(b"quit\r\n")
			self.print_send_msg( "quit\r\n")
			self.print_recv_msg(client_socket)


	def establish_socket_connection(self):
		client_socket = socket(AF_INET,SOCK_STREAM)
		client_socket.connect(self.mail_server)
		self.print_recv_msg(client_socket)
		if self.starttls == True:
			client_socket.send(b"ehlo "+ self.helo +b"\r\n")
			self.print_send_msg("ehlo "+ self.helo.decode("utf-8")+"\r\n")
			self.print_recv_msg(client_socket)
			
			client_socket.send(b"starttls\r\n")
			self.print_send_msg("starttls\r\n") 
			self.print_recv_msg(client_socket)

			tls_socket = ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_TLS)
			self.tls_socket = tls_socket

		self.client_socket = client_socket


	def close_socket(self):
		if self.tls_socket != None:
			self.tls_socket.close()
		if self.client_socket != None:
			self.client_socket.close()

	def write_logs(self):
		logs = '\n'.join(str(e) for e in self.screen_report)
		f = open("logs.txt","a")
		f.write("\n----------------------------------------------------------------------\n")
		f.write(logs)
		f.write("\n----------------------------------------------------------------------\n")
		f.close()

	def send_email(self):
		self.establish_socket_connection()

		try:
			if self.starttls == True:
				self.send_smtp_cmds(self.tls_socket)
				self.send_quit_cmd(self.tls_socket)
			else:
				self.send_smtp_cmds(self.client_socket)
				self.send_quit_cmd(self.client_socket)
			if self.blocked_socket == False:
				self.close_socket()
			if self.log == True:
				self.write_logs()
			
			if self.blocked_socket == True:
				return "blocked"
			return ""
		except Exception as e:
			import traceback
			traceback.print_exc()	

	def __del__(self):
		self.close_socket()