import asyncio
import dns
import requests
from pyppeteer import launch
from taser import printx
import json

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

async def checkEmailRep(email):
	browser = await launch()
	page = await browser.newPage()
	await page.goto('https://emailrep.io/')
	await page.evaluate(f"""() => {{
		document.getElementById('search-input').value = '{email}';
	}}""")

	await page.click('#search-form > div > span > button')
	await asyncio.sleep(6)
	reputation_response = await page.querySelector('#api-response')
	final_rep = await page.evaluate('(reputation_response) => reputation_response.textContent', reputation_response)
	await browser.close()
	print(final_rep)


async def checkPowned(email):
	print(email)
	browser = await launch()
	page = await browser.newPage()
	await page.goto('https://haveibeenpwned.io/')
	await page.setUserAgent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
	await page.screenshot({'path': 'example.png'})
	'''await page.evaluate(f"""() => {{
		document.getElementById('Account').value = '{email}';
	}}""")'''

	'''await page.click('#search-form > div > span > button')
	await asyncio.sleep(6)
	reputation_response = await page.querySelector('#api-response')
	final_rep = await page.evaluate('(reputation_response) => reputation_response.textContent', reputation_response)
	await browser.close()
	print(final_rep)



	browser = await launch()
	page = await browser.newPage()
	await page.goto('https://haveibeenpwned.com/')
	await page.evaluate(f"""() => {{
		document.getElementById('Account').value = '{email}';
	}}""")

	await page.click('#searchPwnage')
	await asyncio.sleep(6)
	breaches_powned = await page.querySelector('#pwnedWebsitesContainer > div:nth-child(2)')
	final_breaches = await page.evaluate('(breaches_powned) => breaches_powned.textContent', breaches_powned)
	await browser.close()
	print(final_breaches)'''


def checkRep(email):
	printx.colored("\n[+] Checking email reputation of "+'\033[1m' + str(email) + '\033[1m' +"...",fg="blue")
	#asyncio.get_event_loop().run_until_complete(checkEmailRep(email))
	print("----------------------------------------------------------------")
	asyncio.get_event_loop().run_until_complete(checkPowned(email))

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
	print("\n")
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

	printx.colored("\n[+] Getting blacklist list... ",fg="blue")
	print("\n")
	url2 = "https://api.hetrixtools.com/v2/dc60cd86592d17098de23317368b0de2/blacklist-check/ipv4/"+str(ip)+"/"
	headers = {
    	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
	}
	r_hetrix_tools = requests.get(url2, headers=headers)
	hetrix_data = json.loads(r_hetrix_tools.text)
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
		print("API key ")


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
		printx.colored("[✖] This domain doesn't exist!", fg="red")


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
