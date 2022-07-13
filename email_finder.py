from typing import final
import requests
from taser import printx
import json
import time
import asyncio
import dns
from pyppeteer import launch
import socket
from PyInquirer import prompt
from examples import custom_style_2
from tqdm import tqdm

api_keys1 = ["6d103ea6d5d7d4b0fe81ab23efbf6e79fb2189fe","9c4f2d7d18ecbc378147e5443f76422e50cd13bd","8f1558da76c8bf09a601b9327d09556f864f8880"]
api_keys2 = ["77605d0a-0365-40b2-907e-39ab6e5c59b0","df9c2b7e-408d-41e2-b924-8cc793cb1e79"]
headers = {
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

API_ROOT = 'https://2.intelx.io'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'

def findEmails(domain):
	emails_caught = []
	for key in api_keys1:
		try:
			url = "https://api.hunter.io/v2/domain-search?domain="+domain+"&api_key="+key.strip()
			r = requests.get(url,headers=headers)
			data = json.loads(r.text)
			all_emails = data["data"]["emails"]
			for email in all_emails:
				emails_caught.append(email["value"])
			break
		except:
			pass
	
	return emails_caught

def finishSearch(uuid,api_key):
	h = {'x-key': api_key, 'User-Agent': USER_AGENT}
	r = requests.get(API_ROOT + f'/intelligent/search/terminate?id={uuid}', headers=h)
	if(r.status_code == 200):
		return True
	else:
		return r.status_code

def startSearch(term,api_key, maxresults=100, buckets=[], timeout=5, datefrom="", dateto="", sort=4, media=0, terminate=[], target=0):
	h = {'x-key': api_key, 'User-Agent': USER_AGENT}
	p = {
		"term": term,
		"buckets": buckets,
		"lookuplevel": 0,
		"maxresults": maxresults,
		"timeout": timeout,
		"datefrom": datefrom,
		"dateto": dateto,
		"sort": sort,
		"media": media,
		"terminate": terminate,
		"target": target
	}
	r = requests.post(API_ROOT + '/phonebook/search', headers=h, json=p)
	if r.status_code == 200:
		return r.json()['id']
	else:
		return r.status_code

def getResults(id,api_key, limit=1000, offset=-1):
	h = {'x-key': api_key, 'User-Agent': USER_AGENT}
	r = requests.get(API_ROOT + f'/phonebook/search/result?id={id}&limit={limit}&offset={offset}', headers=h)
	if(r.status_code == 200):
		return r.json()
	else:
		return r.status_code

def queryResults(id, limit,api_key):
	results = getResults(id,api_key,limit)
	return results

def findMoreEmails(term,api_key, maxresults=1000, buckets=[], timeout=5, datefrom="", dateto="", sort=4, media=0, terminate=[], target=0):
	results = []
	results2 = []
	done = False
	search_id = startSearch(term,api_key, maxresults, buckets, timeout, datefrom, dateto, sort, media, terminate, target)
	if(len(str(search_id)) <= 3):
		done = True
	while done == False:
		time.sleep(1)  # lets give the backend a chance to aggregate our data
		r = queryResults(search_id, maxresults,api_key)
		results.append(r)
		maxresults -= len(r['selectors'])
		if(r['status'] == 1 or r['status'] == 2 or maxresults <= 0):
			if(maxresults <= 0):
				finishSearch(search_id,api_key)
			done = True
	#print(results)
	all_emails = results[0]["selectors"]
	for email in all_emails:
		value = email["selectorvalue"]
		results2.append(value)
	return results2


async def website_search(domain):
	browser = await launch()
	page = await browser.newPage()
	await page.goto('https://phonebook.cz/')
	content = domain
	await page.evaluate(f"""() => {{
		document.getElementById('domain').value = '{content}';
	}}""")

	await page.click('#submit1')
	await asyncio.sleep(6)
	emails = await page.querySelector('pre')
	final_emails = await page.evaluate('(emails) => emails.textContent', emails)
	await browser.close()
	return final_emails



def emailFinder(domain):
	domain_existance = True
	try:
		result = socket.gethostbyname(domain)
	except:
		domain_existance = False
	

	if domain_existance == True:
		printx.colored("\n[+] Searching emails for "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
		first_list = findEmails(domain)
		for key in api_keys2:
			try:
				second_list = findMoreEmails(domain,key)
				if len(second_list) != 0:
					break
				else:
					second_list = []
			except:
				pass
		third_list = asyncio.get_event_loop().run_until_complete(website_search(domain))
		if 'Daily limit reached' in str(third_list):
			printx.colored("[✖] Some of the search are failing due to daily rating exceeded, try again in one day an probably more emails will be displayed", fg="red")
			third_list = []
		third_list = third_list.split("\n")
		third_list = third_list[:-1]
		final_list = first_list + second_list + third_list
		printx.colored("[+] Treating data...",fg="blue")
		last_list = []
		#print(final_list)
		for email in final_list:
			if email.find("@") != -1:
				if email.find("http") == -1:
					last_list.append(email)
		final_new_list = list(set(last_list))
		for email in final_new_list:
			print(email)
		printx.colored("\n[✔] Found "+'\033[1m' + str(len(final_new_list)) +" emails" '\033[1m' +"!!",fg="green")
		print("\n")
		questions = [
			{
					'type': 'confirm',
					'message': "You want to save the emails into '.txt' file?",
					'name': 'save_emails',
					'default': True,
			},
			{
					'type': 'confirm',
					'message': "You want to validate if the emails exists?",
					'name': 'validate_emails',
					'default': True,
			}
		]
		email_answers = prompt(questions, style=custom_style_2)
		print("\n")
		domain_file = domain.split(".")
		domain_file = domain[0]
		if email_answers["save_emails"] == True:
			non_validated_emails = '\n'.join(str(e) for e in final_new_list)
			non_validated_file_name = "no_validated_emails_"+str(domain_file)+".txt"
			f = open(non_validated_file_name,"w")
			f.write(non_validated_emails)
			f.close()
			printx.colored("[+] Emails saved in 'no_validated_emails_"+str(domain_file)+".txt'",fg="blue")
		if email_answers["validate_emails"] == True:
			validated_emails = []
			printx.colored("[+] Validating " +'\033[1m' + str(len(final_new_list)) +" email adresses, " '\033[1m' + "this can take a bit long don't close it...\n",fg="blue")
			api_key = "f375b481-a24b-4317-8c1a-f853328f00fc"
			error_validator_counter = 0
			validator_connection = True
			
			for i in tqdm(range(len(final_new_list))):
				try:
					email_address = final_new_list[i].strip()
					params = {'email': email_address}
					headers = {'Authorization': "Bearer " + api_key }
					response = requests.get("https://isitarealemail.com/api/email/validate",params = params, headers = headers)
					status = response.json()['status']
					if status == "valid":
						validated_emails.append(email_address)
					if status == "unknown":
						validated_emails.append(email_address)
				except:
					printx.colored("[+] Error validating: "+str(final_new_list[i].strip()),fg="red")
					error_validator_counter+=1
					if error_validator_counter > 35:
						validator_connection = False
						printx.colored("[+] Validation conenction lost, try again later... ",fg="red")
						break
			if validator_connection !=False:
				printx.colored("\n[✔] Valid emails: "+'\033[1m' + str(len(validated_emails))+"/"+str(len(final_new_list)) + '\033[1m' +"!!",fg="green")
				printx.colored("[+] Emails saved in 'validated_emails_"+str(domain_file)+".txt'",fg="blue")
				validated_final_emails = '\n'.join(str(e) for e in validated_emails)
				validated_file_name = "validated_emails_"+str(domain_file)+".txt"
				f = open(validated_file_name,"w")
				f.write(validated_final_emails)
				f.close()


	else:
		printx.colored("[-] This domain doesn't exist!", fg="red")
