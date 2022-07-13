from multiprocessing.dummy import current_process
from additional.common import *
from additional.sendmail import *
import subprocess
import copy
try:
	import threading
except:
	pass
try:
	from PyInquirer import prompt
except:
	pass
try:
	from check_rep import checkRep,checkIpDomainRep
except:
	pass
from examples import custom_style_2
from doctest import ELLIPSIS_MARKER
import sys
import signal
try:
	from taser import printx
except: 
	pass
import config
import cases
try:	
	from tabulate import tabulate
except:
	pass
from builder import update_cases_info,generate_smtp_seqs
try:
	from concurrent.futures import ThreadPoolExecutor
except:
	pass
import json
try:
	import requests
except:
	pass
try:
	import wget
except:
	pass
import os
try:
	from halo import Halo
except:
	pass
try:
	from webcopy import websiteCopier
except:
	pass
try:
	from check_protocols import securityCheck
except:
	pass
try:
	from email_finder import emailFinder
except:
	pass
try:	
	from similarDomain import sameDomain
except:
	pass
try:
	from datetime import datetime
except:
	pass
sem = threading.Semaphore()

def def_handler(sig, frame):
	printx.colored("\n\n[-] Closing program...\n",fg="red")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)


def end_script():
	printx.colored("\n\n[-] Closing program...\n",fg="red")
	sys.exit(1)




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

def banner():
	print("")
	print("")
	print("                          	██████╗ ██╗   ██╗  ███╗   ███╗ █████╗ ██╗██╗     ")
	print("                          	██╔══██╗╚██╗ ██╔╝  ████╗ ████║██╔══██╗██║██║     ")
	print("                          	██████╔╝ ╚████╔╝   ██╔████╔██║███████║██║██║     ")
	print("                          	██╔══██╗  ╚██╔╝    ██║╚██╔╝██║██╔══██║██║██║     ")
	print("                          	██████╔╝   ██║     ██║ ╚═╝ ██║██║  ██║██║███████╗")
	print("                          	╚═════╝    ╚═╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝")
	print("")
	print( "                              __________________________________________________"		)			
	print( "                                  ︻デ═一  Created by: marcsabate7  ︻デ═一 " )
	print( "          -------------------------------------------------------------------------------------------")
	print( "               		   Any action related to ByMail is only your responsibility")
	print( "          -------------------------------------------------------------------------------------------")
	print("")
	printx.colored(" v0.1.0 ",fg="white",bg="green")

def reportConfig(cases,config,verbose, proxy_list,proxy_file, logs):
	print("")
	col_names = ["Option", "Value"]
	data = []
	mode = config['case_id']
	
	print("Config set:")
	print("")
	if mode.decode("utf-8") not in cases:
		error_message = "* It's not a valid mode, please select one from 'cases.py' or the program will fail"
		final_mode = mode.decode("utf-8")
		final_mode = final_mode +"\n"+ error_message
	else:
		final_mode = mode.decode("utf-8")

	data.append(["Mode ID", final_mode])

	emails = read_user_emails()
	if len(emails) == 0:
		final_emails = "0+\n" +"* Users file is empty, please add almost one user or the program will fail"
	else:
		final_emails = len(emails)

		f = open("users.txt","r")
		all_emails = f.readlines()[0:10]
		all_emails = ''.join([str(email) for email in all_emails])
		if final_emails > 10:
			final_emails = str(final_emails) + "  -  Only showing the firts 10 emails" 
		final_emails = str(final_emails) + "\n\n" + str(all_emails)

	data.append(["Emails uploaded", final_emails])


	data.append(["Sending emails as", str(config["legitimate_site_address"].decode("utf-8"))])

	tls_cipher = config["server_mode"]["starttls"]
	if tls_cipher == True:
		tls_cipher = "Activated"
	else:
		tls_cipher = "Desactivated"
	data.append(["TLS chiper", tls_cipher])

	if proxy_list == True:
		if proxy_file == True:
			proxy = "Activated"
		else:
			proxy = "Activated" + "\n" + "* The file you set is incorrect, please set a correct name file or the program will fail"
	else:
		proxy = "Desactivated"
	data.append(["Proxies", proxy])

	if logs == True:
		logs = "Activated" + "\n" + "Will be saved in 'logs.txt' file at the same directory"
	else:
		logs = "Desactivated"
	data.append(["Record logs", logs])

	if verbose == True:
		verbose_mode = "Activated"
	else:
		verbose_mode = "Desactivated"
	data.append(["Verbose mode", verbose_mode])

	print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))
	print("\n")
	
	printx.colored("* To use logs or threads take a look to the help panel!", fg="purple")
	print("\n")

def showTemplates():
		questions = [
			{
				'type': 'list',
				'name': 'option',
				'message': 'Select template',
				'choices': [
					'1) Adobe',
					'2) Amazon',
					'3) Badoo',
					'4) Discord',
					'5) Ebay',
					'6) Facebook',
					'7) FB_messenger',
					'8) Freefire',
					'9) Github',
					'10) Gitlab',
					'11) Google',
					'12) Google_new',
					'13) Google_poll',
					'14) Icloud',
					'15) Instagram',
					'16) Linkedin',
					'17) Mediafire',
					'18) Messenger',
					'19) Netflix',
					'20) Outlook',
					'21) Playstation',
					'22) ProtonMail',
					'23) Reddit',
					'24) Shopify',
					'25) Snapchat',
					'26) Snapchat2',
					'27) Socialclub',
					'28) Spotify',
					'29) StackOverflow',
					'30) Steam',
					'31) Telegram',
					'32) Tiktok',
					'33) Twitch',
					'34) Twitter',
					'35) Wordpress',
					'36) Xbox',
					'37) Yahoo',
					'38) Yandex',
					'39) Youtube',
					'40) Go back'
				]
			}
		]

		answers2 = prompt(questions, style=custom_style_2)
		answer = answers2["option"]
		if answer == "40) Go back":
			pass
		else:
			answer = answers2["option"].split(" ")
			answer = answer[1]
			answer = answer.lower()
			printx.colored("[+] Starting downloading template: "+'\033[1m' + str(answer) + '\033[1m' +"...",fg="blue")

			url = "https://github.com/marcsabate7/Files/raw/main/phishing_templates/"+str(answer)+".zip"
			try:
				file = wget.download(url)
				printx.colored("\n\n[✔] Template downloaded succesfully!",fg="green")
				print("  - Saved in the same directory as: "+'\033[1m' + str(answer) + ".zip"+'\033[1m' +"...")
			except:
				printx.colored("[-] An error has ocurred when downloading the template, try again later...",fg="red")
			print("\n")
		

def showPayloads():
	print("\n")
	print("List of payloads:")

def helpPanel():
	print("\n")
	print("Help panel:\n")
	print("                       ==============================================================")
	printx.colored("                                                   Utilities",fg="purple")
	print("                       ==============================================================")
	print("                       [-t <num threads>] Threads to use (10 is recommended)")
	print("                       [-proxy <file>] Proxy list, each email will be send with different IP")
	print("                       [-l] Log generator, logging all sockets data")
	print("                       [-templates] Examples for email templates")
	print("                       [-payloads] Show different payloads to use")
	print("                       [-h/-help] Show this help panel and exit")
	print("                       ==============================================================")
	printx.colored("                                               Lookup your config",fg="purple")
	print("                       ==============================================================")
	print("                       [-lookup] Show config, users and mode that are now set")
	print("                       ==============================================================")
	printx.colored("                                                   Examples",fg="purple")
	print("                       ==============================================================")
	print("                       Full command line mode:")
	print("                         - Example 1: python bymail.py -t 10 -v")
	print("                         - Example 2: python bymail.py -t 3 -l -v")
	print("                         - Example 3: python bymail.py -t 3 -l -v -proxy proxies.txt")
	print("                         - Example 4: python bymail.py -templates")
	print("                         - Example 5: python bymail.py -payloads")
	print("                         - Example 5: python bymail.py -lookup")
	printx.colored("                         * Use this mode to run directly the program!",fg="blue")
	print("")
	print("                       Step by step mode:")
	print("                         - Example 1: python bymail.py")
	printx.colored("                         * You only need to follow program instructions step by step!",fg="blue")
	print("                       ==============================================================")
	print("")
	print("")



def parse_args():
	verbose = False
	proxy_list = False
	proxy_file = False
	logs = False
	threads_incorrect = False
	threads = False
	num_threads = 1
	args_counter = 0
	print("\n")
	arguments = sys.argv[1:]
	for argument in arguments:
		if argument == '-h' or argument == '-help':
			helpPanel()
			sys.exit()
		if argument == '-templates':
			showTemplates()
			sys.exit(1)
		if argument == '-payloads':
			showPayloads()
			sys.exit(1)
		if argument == '-t':
			args_counter+=1
			threads = True
			file_index = arguments.index("-t") + 1
			num_threads = arguments[file_index]
			try:
				num_threads = int(num_threads)
			except:
				threads_incorrect = True

		if argument == '-proxy':
			args_counter+=1
			proxy_list = True	
			#print(arguments)
			file_index = arguments.index("-proxy") + 1
			try:
				f = open(arguments[file_index]+".txt","r")
				f.close()
				proxy_file = True
			except:
				#print("The file you want to use with proxies does not exist")
				proxy_file = False
		if argument == '-l':
			logs = True


	if '-lookup' in arguments:
		reportConfig(cases.cases,config.config,True, proxy_list,proxy_file,logs)
		sys.exit(1)

	args = {
		"verbose": verbose,
		"proxy": proxy_list,
		"proxy_file":proxy_file,
		"logs": logs,
		"num_threads":num_threads,
		"threads_incorrect":threads_incorrect, 
		"args_counter":args_counter
	}


	return args


def changeData():
	questions = [
		{
			'type': 'confirm',
			'message': 'Input sender email address (Fake address)',
			'name': 'chiper',
			'default': True,
		},
		{
			'type': 'confirm',
			'message': "Input email subject",
			'name': 'logs',
			'default': True,
		},
		{
			'type': 'input',
			'message': 'Num threads (Default 2):',
			'name': 'num_threads',
			'default': "2",
		},
		{
			'type': 'input',
			'message': 'Input proxies file name if you want to use proxies, if not leave it blank:',
			'name': 'proxy_file',
			'default': "",
		}
	]

	changing_data_answers = prompt(questions, style=custom_style_2)

def check_config(verbose, proxy_list,proxy_file, logs, num_threads, threads_incorrect,config,cases):
	errors_detected = False
	col_names = ["Option", "Value"]
	data = []
	mode = config['case_id']

	print("Config set:")
	print("")

	if mode.decode("utf-8") not in cases:
		error_message = "* It's not a valid mode, please select one from 'cases.py' or the program will fail"
		final_mode = mode.decode("utf-8")
		final_mode = final_mode +"\n"+ error_message
		errors_detected = True
	else:
		final_mode = mode.decode("utf-8")

	data.append(["Mode ID", final_mode])

	emails = read_user_emails()
	if len(emails) == 0:
		final_emails = "0+\n" +"* Users file is empty, please add almost one user or the program will fail"
		errors_detected = True
	else:
		final_emails = len(emails)

	data.append(["Emails uploaded", final_emails])


	data.append(["Sending emails as", str(config["legitimate_site_address"].decode("utf-8"))])

	if threads_incorrect == True:
		threads_message = "* Please set a correct value for a number of threads, or recommendation is to set in 10 if you have to send a lot of emails"
		errors_detected = True
	else:
		num_threads = int(num_threads)
		if num_threads > 10:
			threads_message = str(num_threads) + "\n" + "* Our recommendation is to set it to 10 or minor, run it at your own risk"
		else:
			threads_message = num_threads
	data.append(["Number of threads", threads_message])

	tls_cipher = config["server_mode"]["starttls"]
	if tls_cipher == True:
		tls_cipher = "Activated"
	else:
		tls_cipher = "Desactivated"
	data.append(["TLS chiper", tls_cipher])

	if proxy_list == True:
		if proxy_file == True:
			proxy = "Activated"
		else:
			proxy = "Activated" + "\n" + "* The file you set is incorrect, please set a correct name file or the program will fail"
			errors_detected = True
	else:
		proxy = "Desactivated"
	data.append(["Proxies", proxy])

	if logs == True:
		logs = "Activated" + "\n" + "Will be saved in 'logs.txt' file at the same directory"
	else:
		logs = "Desactivated"
	data.append(["Record logs", logs])

	if verbose == True:
		verbose_mode = "Activated"
	else:
		verbose_mode = "Desactivated"
	data.append(["Verbose mode", verbose_mode])

	print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))


	if errors_detected == True:
		printx.colored("\n\n[-] Invalid configuration detected, fix it before continue...\n",fg="red")
		sys.exit(1)

def threadExecution(victim_email,num_thread,total_threads,verbose_mode,log_mode,config): # Aqui haurem de pasar la config
	not_exist_domain = False
	prova = int(num_thread) % int(total_threads)
	if prova == 0:prova = total_threads

	dt_string = get_current_date()
	sem.acquire()
	print("[Thread "+str(prova)+" - "+str(dt_string)+"]  " +color.BLUE +"Sending email to: "+ color.END + color.BOLD+str(victim_email)+color.END)
	sem.release()
	if verbose_mode == True:
		dt_string = get_current_date()
		sem.acquire()
		print("[Thread "+str(prova)+" - "+str(dt_string)+"]  " +color.BLUE+"Getting MX IP address for domain..."+color.END)
		sem.release()
	domain = victim_email.split("@")[1]


	mail_server_ip = get_mail_server_from_email_address(domain)
	if mail_server_ip == "non-exist-domain": 
		dt_string = get_current_date()
		sem.acquire()
		print("[Thread "+str(prova)+" - "+str(dt_string)+"]  " +color.RED +"Couldn't get MX IP address for domain " +str(domain)+", killing thread..."+color.END)
		not_exist_domain = True

	if not_exist_domain == False:
		if verbose_mode == True:
			dt_string = get_current_date()
			sem.acquire()
			print("[Thread "+str(prova)+" - "+str(dt_string)+"]  " +color.GREEN +"Victim server IP address obtained: "+ color.END+color.BOLD +str(mail_server_ip)+color.END)
			sem.release()
		

		mail_server_port = config["server_mode"]['recv_mail_server_port']
		starttls = config['server_mode']['starttls']

		news_cases = copy.deepcopy(cases.cases)

		different_return = update_cases_info(news_cases,victim_email,config)
		if verbose_mode == True:
			dt_string = get_current_date()
			sem.acquire()
			print("[Thread "+str(prova)+" - "+str(dt_string)+"]  " +color.BLUE +"Generating SMTP data sequence..."+color.END)
			sem.release()

		smtp_seqs = generate_smtp_seqs(different_return)

		message_content = smtp_seqs["msg_content"]

		if verbose_mode == True:
			dt_string = get_current_date()
			sem.acquire()
			print("[Thread "+str(prova)+" - "+str(dt_string)+"]  " +color.YELLOW +"Opening socket and sending data..."+color.END)
			sem.release()
		# Mirar de pasar el verbose mode i el log mode per controlarho des de els sockets
		# Mirar de utilitzar socksiPy

		send_mail = SendMail()
		send_mail.set_mail_info((mail_server_ip, mail_server_port),helo=smtp_seqs["helo"], mail_from=smtp_seqs["mailfrom"], rcpt_to =smtp_seqs["rcptto"], email_data=message_content, starttls=starttls,verbose = verbose_mode, log = log_mode,num_thread = prova)
		status_return = send_mail.send_email()

		dt_string = get_current_date()
		sem.acquire()
		if status_return != "blocked":
			print("[Thread "+str(prova)+" - "+str(dt_string)+"]  " +color.GREEN +"Email sent successfully to: "+color.END + color.BOLD +str(victim_email) +color.END)
		sem.release()


def executor(num_threads,emails,verbose,logs,config):
	with ThreadPoolExecutor(max_workers=num_threads) as executor:                                                
		[executor.submit(threadExecution, emails[i],i+1,num_threads, verbose,logs,config) for i in range(len(emails))]

def configurationMenu():
	exit_loop2 = False
	while exit_loop2 == False:
		questions = [
			{
				'type': 'list',
				'name': 'option',
				'message': 'Choose an option?',
				'choices': [
					'1) Help',
					'2) View templates',
					'3) View payloads',
					'4) View victim emails',
					'5) Change sender information',
					'6) Check all configuration set',
					'7) Go back'
				]
			}
		]

		answers2 = prompt(questions, style=custom_style_2)
		if answers2['option'] == "1) Help":
			helpPanel()
			print("\n")

		if answers2['option'] == "2) View templates":
			showTemplates()

		if answers2['option'] == "3) View payloads":
			showPayloads()

		if answers2['option'] == "4) View victim emails":
			data = []
			col_names = ["Option", "Value"]
			emails = read_user_emails()
			if len(emails) == 0:
				printx.colored("\n\n[-] Users file is empty, please add victim emails to 'user.txt' file!\n",fg="red")
			else:
				final_emails = len(emails)
				f = open("users.txt","r")
				all_emails = f.readlines()[0:10]
				all_emails = ''.join([str(email) for email in all_emails])
				if final_emails > 50:
					final_emails = str(final_emails) + "  -  Only showing the firts 50 emails" 
				final_emails = str(final_emails) + "\n" + str(all_emails)

			data.append(["Emails uploaded", final_emails])
			print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))
			print("\n")

		if answers2['option'] == "5) Change sender information":
			changeData()

		if answers2['option'] == "6) Check all configuration set":
			reportConfig(config.config,cases.cases,False,False,False,False)
			print("\n")
			
		if answers2['option'] == "7) Go back":
			exit_loop2 = True



def optionsMenu():
	exit_loop = False
	while exit_loop == False:
		questions = [
			{
				'type': 'list',
				'name': 'option',
				'message': 'Choose an option?',
				'choices': [
					'1) Send emails (manual configuration)',
					'2) Website cloner',
					'3) Get emails from domain',
					'4) Check domain security (SPF,DMARC,DKIM,BIMI...)',
					'5) Check IP/domain reputation',
					'6) Check email reputation',
					"7) Get similar DOMAIN's & availavility",
					'8) Configuration',
					'9) Exit'
				]
			}
		]
		
		answers = prompt(questions, style=custom_style_2)

		if answers['option'] == "1) Send emails (manual configuration)":
			# Preparar preguntes per verbose y mes de ferho manual
			exit_loop = True
			# Mirar si afegir el SENDER i el MODE as en aquestes preguntes ja que esta amb bytes i hem de mirar de arreglarho
			questions = [
				{
					'type': 'confirm',
					'message': 'You want to chiper emails with TLS?',
					'name': 'chiper',
					'default': True,
				},
				{
					'type': 'confirm',
					'message': "Log mode (Save sockets send/receive data in a 'log.txt' file)?",
					'name': 'logs',
					'default': True,
				},
				{
					'type': 'input',
					'message': 'Num threads (Default 2):',
					'name': 'num_threads',
					'default': "2",
				},
				{
					'type': 'input',
					'message': 'Input proxies file name if you want to use proxies, if not leave it blank:',
					'name': 'proxy_file',
					'default': "",
				}
			]

			manual_config_answers = prompt(questions, style=custom_style_2)
			return manual_config_answers

		if answers['option'] == "2) Website cloner":
			questions = [
				{
					'type': 'input',
					'message': 'Input URL to clone:',
					'name': 'website_url',
					'default': "",
				}
			]
			website_cloner_answers = prompt(questions, style=custom_style_2)
			websiteCopier(website_cloner_answers["website_url"])
			sys.exit(0)

		if answers['option'] == "3) Get emails from domain":
			questions = [
				{
					'type': 'input',
					'message': 'Input domain:',
					'name': 'domain_check',
					'default': "",
				}
			]
			finder_emails = prompt(questions, style=custom_style_2)
			emailFinder(finder_emails["domain_check"])
			print("\n")

		if answers['option'] == "4) Check domain security (SPF,DMARC,DKIM,BIMI...)":
			questions = [
				{
					'type': 'input',
					'message': 'Input domain to check:',
					'name': 'domain_check',
					'default': "",
				}
			]
			domain_checker_answers = prompt(questions, style=custom_style_2)
			securityCheck(domain_checker_answers["domain_check"])
			print("\n")
	
		if answers['option'] == "5) Check IP/domain reputation":
			questions = [
				{
					'type': 'input',
					'message': 'Input IP or domain to check:',
					'name': 'ip_check',
					'default': "",
				}
			]
			ip_domain_checker = prompt(questions, style=custom_style_2)
			checkIpDomainRep(ip_domain_checker["ip_check"])
			print("\n")
	
		if answers['option'] == "6) Check email reputation":
			questions = [
				{
					'type': 'input',
					'message': 'Input email to check:',
					'name': 'email_check',
					'default': "",
				}
			]
			email_checker = prompt(questions, style=custom_style_2)
			checkRep(email_checker["email_check"])
			print("\n")
	
		if answers['option'] == "7) Get similar DOMAIN's & availavility":
			questions = [
				{
					'type': 'input',
					'message': 'Input domain:',
					'name': 'similar_domain',
					'default': "",
				}
			]
			domain_name = prompt(questions, style=custom_style_2)
			sameDomain(domain_name["similar_domain"])
			print("\n")
	
		if answers['option'] == "8) Configuration":
			configurationMenu()

		if answers['option'] == "9) Exit":
			end_script()

def checkModules():
	modules_list = ["dns","emailrep","halo","PyInquirer","pyppeteer","pywebcopy","requests","tabulate","taser","tqdm","tweepy","wget"]
	for module in modules_list:
		command = "import "+str(module)
		try:
			with open(os.devnull, 'wb') as devnull:
				p = subprocess.check_call(['python', '-c',str(command)], stdout=devnull, stderr=subprocess.STDOUT)
		except:
			printx.colored("[!] Modules missing, proceeding to the installation...",fg="red")
			print("[+] Installing "+ str(module)+" module...")
			try:
				with open(os.devnull, 'wb') as devnull:
					p = subprocess.check_call(['pip3', 'install',str(module)], stdout=devnull, stderr=subprocess.STDOUT)
			except:
				printx.colored("[!] You don't have pip/pip3 for python installed, please install it before start!",fg="red")
				sys.exit(1)

		
def main():
	checkModules()
	banner()

	args = parse_args()
	if args["args_counter"] == 0:
		args = optionsMenu()
		#print(args)

		proxy = False
		if args["proxy_file"] != "":
			proxy = True
		try:
			threads_incorrect = False
			args["num_threads"] = int(args["num_threads"])
		except:
			threads_incorrect = True

		chiper_status = args["chiper"]
		configuration = config.config
		#print(configuration)
		#config_json = json.load(configuration)
		configuration["server_mode"]["starttls"] = chiper_status

		print("\n")
		# ARREGLAR AQUI, FICAR COMPROBACIÓ DIRECTAMENT
		emails = read_user_emails()
		if len(emails) == 0:
			while True:
				emails = read_user_emails()
				if len(emails) !=0:
					printx.colored("Victim emails uploaded succesfully...!",fg="green")
					break
				printx.colored("Add victim emails to the users.txt file before continue...",fg="red")
				time.sleep(5)
		check_config(True,proxy,args["proxy_file"],args["logs"], args["num_threads"], threads_incorrect,configuration,cases.cases)

	else:
		configuration = config.config
		check_config(True,args["proxy"],args["proxy_file"],args["logs"], args["num_threads"], args["threads_incorrect"],configuration,cases.cases)
	

	print("\n")

	with Halo(text='Press enter key to start sending emails...', spinner='dots'):
		input("Press any key to start sending emails...")
	
	print("\n")
	
	printx.colored("[+] Starting sending emails...\n",fg="green")
	print("\n")

	emails = read_user_emails()

	last_victim_email = "victim@victim.com"

	executor(args["num_threads"],emails, True,args["logs"],configuration)

	sys.exit()
	for victim_email in emails:
		print("[+] Sending email to: "+'\033[1m' + str(victim_email) + '\033[0m')
		domain = victim_email.split("@")[1]
		mail_server_ip = get_mail_server_from_email_address(domain)
		print(mail_server_ip)
		mail_server_port = config["server_mode"]['recv_mail_server_port']
		starttls = config['server_mode']['starttls']

		builder_obj = Builder(cases,config,victim_email,last_victim_email)
		smtp_seqs = builder_obj.generate_smtp_seqs()

		message_content = smtp_seqs["msg_content"]

		send_mail = SendMail()
		send_mail.set_mail_info((mail_server_ip, mail_server_port),helo=smtp_seqs["helo"], mail_from=smtp_seqs["mailfrom"], rcpt_to =smtp_seqs["rcptto"], email_data=message_content, starttls=starttls,verbose = args["verbose"])
		send_mail.send_email()
		last_victim_email = victim_email
		printx.colored("[✔] Email sent succesfully to: "+str(victim_email),fg="green")
		print("\n")

if __name__ == '__main__':
	main()