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
from progress.spinner import MoonSpinner 


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
	print( "                                ︻デ═一  Created by: marcsabate7 v1.0  ︻デ═一 " )
	print( "          -------------------------------------------------------------------------------------------")
	print( "               		   Any action related to ByMail is only your responsibility")
	print( "          -------------------------------------------------------------------------------------------")


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

def showTemplates():
	print("\n")
	print("List of templates to use:")

def showPayloads():
	print("\n")
	print("List of payloads to use:")

def parse_args():
	verbose = False
	proxy_list = False
	proxy_file = False
	logs = False
	print("\n")
	arguments = sys.argv[1:]
	for argument in arguments:
		if argument == '-h':
			print("Help panel:\n")
			print("                       ==============================================================")
			print("                                                    Utilities")
			print("                       ==============================================================")
			print("                       [-v] Verbose mode reporting all steps and status")
			print("                       [-proxy <file>] Proxy list, each email will be send with different IP")
			print("                       [-l] Log generator, logging all steps and reports")
			print("                       [-t] Examples for email templates")
			print("                       [-p] Show different payloads to use")
			print("                       [-h] Show this help panel and exit")
			print("                       ==============================================================")
			print("                                               Lookup your config")
			print("                       ==============================================================")
			print("                       [-lookup] Show config, users and mode that are now set")
			print("                       ==============================================================")
			print("")
			print("")
			sys.exit(1)

		if argument == '-t':
			showTemplates()
			sys.exit(1)
		if argument == '-p':
			showPayloads()
			sys.exit(1)
		if argument == '-v':
			verbose = True
		if argument == '-proxy':
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
	}


	return args

def end_script():
	printx.colored("\n\n[-] Closing program...\n",fg="red")
	sys.exit(1)

def check_config(verbose, proxy_list,proxy_file, logs):
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

def main():
	banner()
	
	args = parse_args()
	check_config(args["verbose"],args["proxy"],args["proxy_file"],args["logs"])
	print("\n")

	input("Press any key to start sending emails...")
	print("\n")
	
	printx.colored("[+] Starting sending emails...\n")
	print("\n")
	
	emails = read_user_emails()

	last_victim_email = "victim@victim.com"

	for victim_email in emails:
		print("[+] Sending email to: "+'\033[1m' + str(victim_email) + '\033[0m')
		domain = victim_email.split("@")[1]
		mail_server_ip = get_mail_server_from_email_address(domain)

		mail_server_port = config["server_mode"]['recv_mail_server_port']
		starttls = config['server_mode']['starttls']

		builder_obj = Builder(cases,config,victim_email,last_victim_email)
		smtp_seqs = builder_obj.generate_smtp_seqs()

		message_content = smtp_seqs["msg_content"]

		send_mail = SendMail()
		send_mail.set_mail_info((mail_server_ip, mail_server_port),helo=smtp_seqs["helo"], mail_from=smtp_seqs["mailfrom"], rcpt_to =smtp_seqs["rcptto"], email_data=message_content, starttls=starttls,verbose = args.v)
		send_mail.send_email()
		last_victim_email = victim_email
		printx.colored("[✔] Email sent succesfully to: "+str(victim_email),fg="green")
		print("\n")
if __name__ == '__main__':
	main()