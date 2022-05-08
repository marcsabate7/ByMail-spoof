from examples import custom_style_2
import sys
from time import gmtime, strftime
import base64
import dns.resolver
from time import gmtime, strftime
import random
import string
import traceback

def bs64encode(value):
	return b"=?utf-8?B?"+ base64.b64encode(value) + b"?="


def id_generator(size=6):
	chars=string.ascii_uppercase + string.digits
	return (''.join(random.choice(chars) for _ in range(size))).encode("utf-8")


def get_date():
	mdate= strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
	return (mdate).encode("utf-8")


def query_mx_record(domain):
	try:
		mx_answers = dns.resolver.query(domain, 'MX')
		for rdata in mx_answers:
			a_answers = dns.resolver.query(rdata.exchange, 'A')
			for data in a_answers:
				return str(data)
	except Exception as e:
		traceback.print_exc()


def get_mail_server_from_email_address(domain):
	return query_mx_record(domain)


def read_user_emails():
	emails_list = open("users.txt",'r')
	emails = []
	for email in emails_list.readlines():
		emails.append(email.strip())
	emails_list.close()
	return emails


def update_info(input, old, new):
	if isinstance(input, dict):
		items = list(input.items())
	elif isinstance(input, (list, tuple)):
		items = enumerate(input)
	else:
		return input.replace(old, new)

	for key, value in items:
		input[key] = update_info(value, old, new)
	return input

