from __future__ import print_function, unicode_literals

from pprint import pprint

from PyInquirer import prompt, Separator

from examples import custom_style_2

from doctest import ELLIPSIS_MARKER
from email import message
import sys
import argparse
import signal

from taser import printx

import config
import cases
from additional.common import *
from additional.sendmail import *
from tabulate import tabulate
from builder import Builder
#from progress.spinner import MoonSpinner 
import threading
from concurrent.futures import ThreadPoolExecutor
import json

cases = cases.cases
config = config.config



def def_handler(sig, frame):
	printx.colored("\n\n[-] Closing program...\n",fg="red")
	sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)


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

def reportConfig(verbose, proxy_list,proxy_file, logs):
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
	
	printx.colored("* To use verbose, logs or threads take a look to the help panel!", fg="purple")
	print("\n")

def showTemplates():
	print("\n")
	print("List of templates:")

def showPayloads():
	print("\n")
	print("List of payloads:")

def helpPanel():
	print("\n")
	print("Help panel:\n")
	print("                       ==============================================================")
	printx.colored("                                                    Utilities",fg="purple")
	print("                       ==============================================================")
	print("                       [-t <num threads>] Threads to use (10 is recommended)")
	print("                       [-v] Verbose mode reporting all steps and status")
	print("                       [-proxy <file>] Proxy list, each email will be send with different IP")
	print("                       [-l] Log generator, logging all steps and reports")
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
		if argument == '-v':
			verbose = True
			args_counter+=1
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
		reportConfig(verbose, proxy_list,proxy_file,logs)
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

def end_script():
	printx.colored("\n\n[-] Closing program...\n",fg="red")
	sys.exit(1)

def check_config(verbose, proxy_list,proxy_file, logs, num_threads, threads_incorrect):
	errors_detected = False
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

def threadExecution(emails, victim_email, email_number, verbose_mode):
	print("[Thread "+ str(email_number+1)+"] "+ victim_email)
	sys.exit(1)
	if email_number == 0:
		last_victim_email = "victim@victim.com"
	else:
		last_victim_email = emails[email_number-1]
	print("["+ str(email_number+1)+"]  Sending email to: "+'\033[1m' + str(victim_email) + '\033[0m')
	domain = victim_email.split("@")[1]
	mail_server_ip = get_mail_server_from_email_address(domain)
	#print(mail_server_ip)
	mail_server_port = config["server_mode"]['recv_mail_server_port']
	starttls = config['server_mode']['starttls']

	builder_obj = Builder(cases,config,victim_email,last_victim_email)
	smtp_seqs = builder_obj.generate_smtp_seqs()

	smtp_seqs = str(smtp_seqs)	# eliminar aquesta linia
	#print("["+ str(email_number+1)+ "]" +smtp_seqs)

	message_content = smtp_seqs["msg_content"]
	message_content = str(message_content)	# eliminar aquesta linia
	#print("["+ str(email_number+1)+ "]" +message_content)
	time.sleep(5)
	sys.exit(1)
	send_mail = SendMail()
	send_mail.set_mail_info((mail_server_ip, mail_server_port),helo=smtp_seqs["helo"], mail_from=smtp_seqs["mailfrom"], rcpt_to =smtp_seqs["rcptto"], email_data=message_content, starttls=starttls,verbose = verbose_mode)
	send_mail.send_email()
	last_victim_email = victim_email
	printx.colored("[✔] Email sent succesfully to: "+str(victim_email),fg="green")
	print("\n")

def executor(num_threads,emails, verbose):
	with ThreadPoolExecutor(max_workers=num_threads) as executor:                                                
		[executor.submit(threadExecution,emails, emails[i],i, verbose)for i in range(len(emails))]

def optionsMenu():
	exit_loop = False
	while exit_loop == False:
		questions = [
			{
				'type': 'list',
				'name': 'option',
				'message': 'Choose an option?',
				'choices': [
					'1) Manual configuration for sending emails',
					'2) View victim emails',
					'3) Get emails from domain',
					'4) View all configuration',
					'5) View default templates',
					'6) View payloads',
					'7) Help',
					'8) Exit program',
				]
			}
		]

		answers = prompt(questions, style=custom_style_2)

		if answers['option'] == "1) Manual configuration for sending emails":
			# Preparar preguntes per verbose y mes de ferho manual
			exit_loop = True
			questions = [
				{
					'type': 'confirm',
					'message': 'Verbose mode (report info while execution)?',
					'name': 'verbose',
					'default': True,
				},
				{
					'type': 'confirm',
					'message': 'Log mode?',
					'name': 'logs',
					'default': True,
				},
				{
					'type': 'input',
					'message': 'Num threads (Default 1):',
					'name': 'num_threads',
					'default': "1",
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

		if answers['option'] == "2) View victim emails":
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

		if answers['option'] == "3) Get emails from domain":
			print("Under development")
			print("\n")
		if answers['option'] == "4) View all configuration":
			reportConfig(False,False,False,False)
			print("\n")

		if answers['option'] == "5) View default templates":
			showTemplates()
			print("\n")

		if answers['option'] == "6) View payloads":
			showPayloads()
			print("\n")

		if answers['option'] == "7) Help":
			helpPanel()
			print("\n")

		if answers['option'] == "8) Exit program":
			end_script()

def main():
	banner()
	
	args = parse_args()
	if args["args_counter"] == 0:
		args = optionsMenu()
		proxy = False
		if args["proxy_file"] != "":
			proxy = True
		try:
			threads_incorrect = False
			args["num_threads"] = int(args["num_threads"])
		except:
			threads_incorrect = True
		check_config(args["verbose"],proxy,args["proxy_file"],args["logs"], args["num_threads"], threads_incorrect)
	else:
		check_config(args["verbose"],args["proxy"],args["proxy_file"],args["logs"], args["num_threads"], args["threads_incorrect"])
	

	print("\n")

	from halo import Halo

	with Halo(text='Press enter key to start sending emails...', spinner='dots'):
		input("Press any key to start sending emails...")
	
	print("\n")
	
	printx.colored("[+] Starting sending emails...\n",fg="green")
	print("\n")

	emails = read_user_emails()

	last_victim_email = "victim@victim.com"

	executor(args["num_threads"],emails, args["verbose"])
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