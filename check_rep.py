import asyncio
import dns
import requests
from taser import printx
import json
from emailrep import EmailRep

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

def checkEmailRep(email):
	em_rep_keys = ["nwv7sgwxk9vsx4j7wu7g86g1yodwwgrz8ahz52wpf01v2xnk"]

	for key in em_rep_keys:
		emailrep = EmailRep(key)
		result = emailrep.query(email)
		if len(result) == 6:
			email = result["email"]
			reputation = result["reputation"]
			blacklisted = result["details"]["blacklisted"]
			malicious_activity = result["details"]["malicious_activity"]
			creds_leaked = result["details"]["credentials_leaked"]
			num_leaked = result["references"]
			first_seen = result["details"]["first_seen"]
			last_seen = result["details"]["last_seen"]
			spoofable = result["details"]["spoofable"]

			print("\n")
			print("Information obtained:")
			print("--------------------------")
			print(    color.BOLD + '   Email scanned: ' + color.END+ str(email))
			print(    color.BOLD + '   Suspicious: ' + color.END)
			if blacklisted == False:
				printx.colored("     [✔] This email is not blacklisted",fg="green")
				printx.colored("     [✔] This email is not suspicious and don't have malicious activity",fg="green")
			else:
				printx.colored("   [!] Blacklisted: "+str(blacklisted), fg="red")
				printx.colored("   [!] Malicious activity: "+str(malicious_activity) , fg="red")
			print(    color.BOLD + '     Reputation: ' + color.END+ str(reputation))
			print(    color.BOLD + '   Credentials: ' + color.END)
			print(    color.BOLD + '     Credientials leaked: ' + color.END+str(creds_leaked))
			print(    color.BOLD + '     Times credentials leaked: ' + color.END+str(num_leaked))
			print(    color.BOLD + '     Date credentials were leaked: ' + color.END+str(first_seen) +" - "+ str(last_seen))
			print(    color.BOLD + '   Debility: ' + color.END)
			print(    color.BOLD + '     Address spoofable: ' + color.END+str(spoofable))
			report_data = True
			break
	if report_data == False:
		printx.colored("[✖] Couldn't get information of this email, try it later...", fg="red")


def checkRep(email):
	printx.colored("\n[+] Checking email reputation of "+'\033[1m' + str(email) + '\033[1m' +"...",fg="blue")
	checkEmailRep(email)
	#print("----------------------------------------------------------------")
	#asyncio.get_event_loop().run_until_complete(checkPowned(email))


def checkIp(ip):
	url = 'https://api.abuseipdb.com/api/v2/check'

	querystring = {
		'ipAddress': ip,
		'maxAgeInDays': '90'
	}
	headers = {
		'Accept': 'application/json',
		'Key': '0cdbdc1c3a12dd54c61ba2168c60706b97d5e613cdda5fe140d194d894f716048f5b55c627b9fcdf'
	}

	try:
		response = requests.get( url=url, headers=headers, params=querystring)

		decodedResponse = json.loads(response.text)
		abuse_percentage = decodedResponse["data"]["abuseConfidenceScore"]
		abuse_percentage = int(abuse_percentage)
		total_reports = decodedResponse["data"]["totalReports"]
		ip_country = decodedResponse["data"]["countryCode"]
		usage_type = decodedResponse["data"]["usageType"]
		internet_service_provider = decodedResponse["data"]["isp"]
		domain = decodedResponse["data"]["domain"]
		hostnames = decodedResponse["data"]["hostnames"]

		print("Information obtained:")
		print("--------------------------")
		if abuse_percentage == 0:
			printx.colored("   [✔] No abuses from this IP detected:  " +str(abuse_percentage) + "%",fg="green")
			printx.colored("   [✔] Total times this IP was reported: "+str(total_reports) ,fg="green")
		else:
			printx.colored("   [!] Abuse: "+str(abuse_percentage)+ "%", fg="red")
			printx.colored("   [!] Total times this IP was reported: "+str(total_reports) , fg="red")
		print(    color.BOLD + '   Country: ' + color.END+ str(ip_country))
		print(    color.BOLD + '   Usage type: ' + color.END+str(usage_type))
		print(    color.BOLD + '   ISP: ' + color.END+str(internet_service_provider))
		print(    color.BOLD + '   Domain: ' + color.END+str(domain))
		hosts = ' / '.join(str(e) for e in hostnames)
		if hosts == "":
			print(    color.BOLD + '   Hosts: ' + color.END+str("-"))
		else:
			print(    color.BOLD + '   Hosts: ' + color.END+str(hosts))

	except:
		printx.colored("[✖] Couldn't get part of information of this IP/DOMAIN, try it later...", fg="red")


	url2 = "https://api.hetrixtools.com/v2/dc60cd86592d17098de23317368b0de2/blacklist-check/ipv4/"+str(ip)+"/"
	headers = {
		"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
	}

	r_hetrix_tools = requests.get(url2, headers=headers)
	hetrix_data = json.loads(r_hetrix_tools.text)

	print("Checking blacklists...")

	if hetrix_data["status"] == "SUCCESS":
		blacklist_count = hetrix_data["blacklisted_count"]
		blacklist_list = hetrix_data["blacklisted_on"]
		backlists_urls = []
		for elem in blacklist_list:
			backlists_urls.append(elem["rbl"])
		black = ' / '.join(str(e) for e in backlists_urls)

		if blacklist_count == 0:
			printx.colored("   [✔] This IP is not blacklisted!",fg="green")
		else:
			printx.colored("   [!] Total blacklists: "+str(blacklist_count), fg="red")
			print(   color.BOLD + '   Blacklists names: ' + color.END+str(black))
	else:
		printx.colored("[✖] Couldn't get part of information of this IP/DOMAIN, try it later...", fg="red")


def checkdomain(domain):
	try:
		result = dns.resolver.resolve(domain, 'A')
		if len(result)!= 0:
			for vals in result:
				ip = vals.to_text()
				checkIp(ip)
		else:
			printx.colored("[✖] Couldn't get the domain IP, try it later...", fg="red")
	except:
		printx.colored("[-] This domain doesn't exist!", fg="red")


def checkIpDomainRep(input):
	element = input.split('.')
	if len(element) > 3:
		printx.colored("\n[+] IP address detected, checking reputation for: "+'\033[1m' + str(input) + '\033[1m' +"...",fg="blue")
		try:
			checkIp(input)
		except:
			printx.colored("[✖] There was a problem checking the IP address, try it later...", fg="red")
	elif len(element) == 2:
		printx.colored("\n[+] Domain detected, checking reputation for: "+'\033[1m' + str(input) + '\033[1m' +"...",fg="blue")
		try:
			checkdomain(input)
		except:
			printx.colored("[✖] There was a problem checking the domain, try it later...", fg="red")
	else:
		printx.colored("[✖] Invalid input detected!", fg="red")
