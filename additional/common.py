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


def get_mail_server_from_email_address(e):
	return query_mx_record(e.decode("utf-8"))


def read_user_emails():
    lista_emails = open("usuarios.txt",'r')
    emails = []
    for email in lista_emails.readlines():
        emails.append(email.strip())
    lista_emails.close()
    return emails