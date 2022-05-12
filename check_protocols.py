from taser import printx
import dns
import requests
import json
from PyInquirer import prompt
from examples import custom_style_2

def checkDmarc(domain):
	printx.colored("\n[+] Testing domain: "+ domain + " for DMARC record...",fg="blue")

	url = "https://api.mxtoolbox.com/api/v1/Lookup/dmarc/?argument="+domain.strip()+"&port=443"
	headers = {
		"Authorization":"76ad213f-524c-4d5c-a2ee-9c4e9de62de0"
	}
	final_dmarc = ""
	r = requests.get(url, headers=headers)
	#print(r.text)
	response = json.loads(r.text)
	try:
		name = response["Warnings"][0]["Name"]
		final_dmarc = final_dmarc + name +"\n"
	except:
		name = ""
	
	try: 
		info = response["Warnings"][0]["Info"]
		final_dmarc = final_dmarc + info +"\n"
	except:
		info = ""

	try:
		dmarc_desc = response["Information"][0]["Description"]
		final_dmarc = final_dmarc + dmarc_desc +"\n"
	except:
		dmarc_desc = ""

	if final_dmarc == "":
			printx.colored("[-] DMARC record not found", fg="red")
	else:
		printx.colored("[+] DMARC record found: ",fg="green")
		print(final_dmarc)

	if name == "DMARC Policy Not Enabled" and "v=DMARC1" in str(dmarc_desc):
		printx.colored("[!!] DMARC policy is not enabled, but there are records!", fg="red")


def checkDkim(domain,selector):
	printx.colored("\n[+] Testing domain: "+ domain + " for DMARC record...",fg="blue")
	print ("Testing domain", domain, "for DKIM record with selector", selector, "...")
	try:
		test_dkim = dns.resolver.resolve(selector + '._domainkey.' + domain , 'TXT')
		for dns_data in test_dkim:
			if 'DKIM1' in str(dns_data):
				printx.colored("[+] DKIM record found: ",fg="green")
				print(dns_data)
	except:
		printx.colored("[-] DKIM record not found, check if you are using the correct selector", fg="red")
		pass


def checkSpf(domain):
	printx.colored("\n[+] Testing domain: "+ domain + " for SPF record...",fg="blue")
	final_spf = ""
	try:
		test_spf = dns.resolver.resolve(domain , 'TXT')
		for dns_data in test_spf:
			if 'spf1' in str(dns_data):
				final_spf = dns_data
				printx.colored("[+] SPF record found: ",fg="green")
				print(final_spf)
		if final_spf == "":
			printx.colored("[-] SPF record not found", fg="red")
	except:
		printx.colored("[-] SPF record not found", fg="red")
		pass


def securityCheck(domain):
	checkSpf(domain)
	print("\n")
	checkDmarc(domain)
	print("\n")
	questions = [
		{
			'type': 'input',
			'message': 'To check DKIM protection, introduce selector (press enter to skip):',
			'name': 'dkim',
			'default': "",
		}
	]
	dkim_answers = prompt(questions, style=custom_style_2)
	if dkim_answers["dkim"] != "":
		checkDkim(domain,kim_answers["dkim"])
	else:
		printx.colored("[-] Skiping DKIM protocol...\n", fg="red")