from taser import printx
import dns
import requests
import json
from PyInquirer import prompt
from examples import custom_style_2
from tabulate import tabulate

def checkGeneralInfo(domain):
	col_names1 = ["A record (IP)"]
	data1 = []

	printx.colored("\n[+] Getting A servers from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
	result = dns.resolver.resolve(domain, 'A')

	if len(result)!= 0:
		for vals in result:
			data1.append([vals.to_text()])
		print(tabulate(data1, headers=col_names1, tablefmt="fancy_grid"))
	else:
		printx.colored("[✖] No A records found for "+'\033[1m' + str(domain) + '\033[1m' +"...", fg="red")
	print("\n")

	col_names2 = ["Preference", "MX Server"]
	data2 = []

	printx.colored("\n[+] Getting MX records from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
	answers = dns.resolver.query(domain, 'MX')
	if len(answers) !=0:
		printx.colored("[✔] Servers found: "+ str(len(answers)),fg="green")
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
		test_dkim = dns.resolver.resolve(selector + '._domainkey.' + domain , 'TXT')
		for dns_data in test_dkim:
			if 'DKIM1' in str(dns_data):
				printx.colored("[✔] DKIM record found: ",fg="green")
				print(dns_data)
	except:
		printx.colored("[✖] DKIM record not found, check if you are using the correct selector", fg="red")
		pass


def checkSpf(domain):
	printx.colored("\n[+] Getting SPF record from "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
	col_names = ["SPF value"]
	data = []
	try:
		test_spf = dns.resolver.resolve(domain , 'TXT')
		for dns_data in test_spf:
			if 'spf1' in str(dns_data):
				data.append([dns_data])
				printx.colored("[✔] SPF record found: ",fg="green")
				print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))
		if len(data) == 0:
			printx.colored("[✖] SPF record not found", fg="red")
	except:
		printx.colored("[✖] SPF record not found", fg="red")
		pass


def securityCheck(domain):
	checkGeneralInfo(domain)
	print("\n")
	checkSpf(domain)
	print("\n")
	checkDmarc(domain)
	print("\n")
	questions = [
		{
			'type': 'input',
			'message': 'To check DKIM protection, introduce selector (press enter to skip):',
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