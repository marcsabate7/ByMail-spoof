from taser import printx
import dns
from dns import resolver
import requests
import json
from PyInquirer import prompt
from examples import custom_style_2
from tabulate import tabulate
import time
import socket
import sys

def checkGeneralInfo(domain):
	col_names1 = ["A record (IP)"]
	data1 = []

	printx.colored("\n[+] Getting A records from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
	result = dns.resolver.query(domain, 'A')

	if len(result)!= 0:
		printx.colored("[✔] A records found: "+ str(len(result)),fg="green")
		for vals in result:
			data1.append([vals.to_text()])
		print(tabulate(data1, headers=col_names1, tablefmt="fancy_grid"))
	else:
		printx.colored("[✖] No A records found for "+'\033[1m' + str(domain) + '\033[1m' +"...", fg="red")


	col_names2 = ["NS Records"]
	data2 = []
	printx.colored("\n[+] Getting NS records from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
	answers = dns.resolver.query(domain, 'NS')
	if len(answers) !=0:
		printx.colored("[✔] NS records found: "+ str(len(answers)),fg="green")
		for answer in answers:
			data = str(answer)
			data2.append([data])
		print(tabulate(data2, headers=col_names2, tablefmt="fancy_grid"))
	else:
		printx.colored("[✖] No NS records found for "+'\033[1m' + str(domain) + '\033[1m' +"...", fg="red")


	col_names2 = ["Priority", "MX Server"]
	data2 = []

	printx.colored("\n[+] Getting MX records from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
	answers = dns.resolver.query(domain, 'MX')
	if len(answers) !=0:
		printx.colored("[✔] MX records found: "+ str(len(answers)),fg="green")
		for answer in answers:
			data = str(answer)
			data = data.split(" ")
			data2.append([data[0], data[1]])
		print(tabulate(data2, headers=col_names2, tablefmt="fancy_grid"))
	else:
		printx.colored("[✖] No MX records found for "+'\033[1m' + str(domain) + '\033[1m' +"...", fg="red")


def checkDmarc(domain):
	printx.colored("\n[+] Getting DMARC records from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")

	url = "https://api.mxtoolbox.com/api/v1/Lookup/dmarc/?argument="+domain.strip()+"&port=443"
	#'https://mxtoolbox.com/api/v1/lookup/bimi/paypal.com';
	headers = {
		"Authorization":"76ad213f-524c-4d5c-a2ee-9c4e9de62de0"
	}
	final_dmarc = []
	r = requests.get(url, headers=headers)
	#print(r.text)
	response = json.loads(r.text)
	try:
		name = response["Warnings"][0]["Name"]
		final_dmarc.append([name])
	except:
		name = ""
	
	try: 
		info = response["Warnings"][0]["Info"]
		final_dmarc.append([info])
	except:
		info = ""

	try:
		dmarc_desc = response["Information"][0]["Description"]
		final_dmarc.append([dmarc_desc])
	except:
		dmarc_desc = ""

	if len(final_dmarc) == 0:
			printx.colored("[✖] DMARC record not found", fg="red")
	else:
		col_names = ["DMARC value"]
		data = []
		printx.colored("[✔] DMARC record found: ",fg="green")
	
		for value in final_dmarc:
			data.append(value)
		print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))

	if name == "DMARC Policy Not Enabled" and "v=DMARC1" in str(dmarc_desc):
		printx.colored("[!!] DMARC policy is not enabled, but there are records!", fg="red")


def checkDkim(domain,selector):
	printx.colored("\n[+] Getting DKIM records for " +'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
	print ("Testing domain", domain, "for DKIM record with selector", selector, "...")
	try:
		test_dkim = dns.resolver.query(selector + '._domainkey.' + domain , 'TXT')
		for dns_data in test_dkim:
			if 'DKIM1' in str(dns_data):
				printx.colored("[✔] DKIM record found: ",fg="green")
				print(dns_data)
	except:
		printx.colored("[✖] DKIM record not found, check if you are using the correct selector", fg="red")
		pass


def checkEmailClient(dns_data):
	# Mirar d'arreglar aixo i ficar str(google.com) in dns_data
	dns_data = str(dns_data)
	client_use = ""
	if dns_data.find('google.com') != -1:
		client_use = "GMAIL.COM"

	if dns_data.find('outlook.com') != -1:
		client_use = "OUTLOOK.COM"

	if dns_data.find('yahoo.com') != -1:
		client_use = "YAHOO.COM"

	if dns_data.find('protonmail') != -1:
		client_use = "PROTONMAIL.COM"

	return client_use



def checkSpf(domain):
	printx.colored("\n[+] Getting SPF record from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
	col_names = ["SPF value"]
	data = []
	try:
		test_spf = dns.resolver.query(domain , 'TXT')
		for dns_data in test_spf:
			if 'spf1' in str(dns_data):
				data.append([dns_data])
				printx.colored("[✔] SPF record found: ",fg="green")
				print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))
				client_email = checkEmailClient(dns_data)
				return client_email
		if len(data) == 0:
			printx.colored("[✖] SPF record not found", fg="red")
	except:
		printx.colored("[✖] SPF record not found", fg="red")
		pass

def checkBimi(domain):
	printx.colored("\n[+] Getting BIMI records from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")

	url = "https://api.mxtoolbox.com/api/v1/Lookup/bimi/?argument="+domain.strip()+"&port=443"
	#'https://mxtoolbox.com/api/v1/lookup/bimi/paypal.com';
	headers = {
		"Authorization":"76ad213f-524c-4d5c-a2ee-9c4e9de62de0"
	}
	final_bimi = []
	col_names = ["BIMI value"]
	data = []
	r = requests.get(url, headers=headers)
	response = json.loads(r.text)
	if len(response["Failed"]) != 0:
		printx.colored("[✖] BIMI record not found", fg="red")
	else:
		printx.colored("[✔] BIMI record found: ",fg="green")

		try:
			if response["Information"][0]["Name"] == "record":
				bimi_record = response["Information"][0]["Description"]
				data.append([bimi_record])
		except: 
			pass
		
		if str("a=") in bimi_record:
			print("[+] "+str(domain)+" is using Verified Mark Certificate (VMC) -> check 'a=' tag in the record below")
		

		print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))


def securityCheck(domain):
	domain_existance = True
	try:
		result = socket.gethostbyname(domain)
	except:
		domain_existance = False
	
	if domain_existance == True:
		checkGeneralInfo(domain)
		client_email = checkSpf(domain)
		checkDmarc(domain)
		checkBimi(domain)
		if client_email != "":
			print("\n")
			printx.colored("[✔] "+domain+" is using "+'\033[1m' + str(client_email) + '\033[1m',fg="green")
		print("\n")
		printx.colored("[+] For get DKIM records is needed the selector from the email header\n", fg="blue")
		questions = [
			{
				'type': 'input',
				'message': 'Introduce selector (press enter to skip):',
				'name': 'dkim',
				'default': ""
				'\n'
			}
		]
		dkim_answers = prompt(questions, style=custom_style_2)
		if dkim_answers["dkim"] != "" and dkim_answers["dkim"] != " " and dkim_answers["dkim"] != "\n":
			checkDkim(domain,dkim_answers["dkim"])
		else:
			printx.colored("[-] Skiping DKIM protocol...\n", fg="red")
			time.sleep(1)
			print("\n")
	else:
		printx.colored("[✖] This domain doesn't exist\n", fg="red")