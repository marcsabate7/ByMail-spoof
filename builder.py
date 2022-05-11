from additional.common import *
import sys
import time

def update_cases_info(cases, victim_email,config):
    final_cases = cases
    final_victim_email = victim_email
    final_config = config

    final_cases = update_info(final_cases, b"attack.com", final_config["attacker_site"])
    final_cases = update_info(final_cases, b"admin@legitimate.com", final_config["legitimate_site_address"])
    legitimate_site = config["legitimate_site_address"].split(b"@")[1]  #comprobar aixo qeu fique un > de mes al final
    final_cases = update_info(final_cases, b"legitimate.com", legitimate_site)
    print(final_cases)
    final_cases = update_info(final_cases, b"victim@victim.com", final_victim_email.encode("utf-8"))
    if final_victim_email == "marcsabate65@outlook.com":
        time.sleep(11)
        print("ya em fet el descans")


    #print(cases)
    return cases


def update_info(input, old, new):
	#print(str(input)+"\n"+str(old) +" / "+str(new)+"\n")
	if isinstance(input, dict):
		items = list(input.items())
	elif isinstance(input, (list, tuple)):
		items = enumerate(input)
	else:
		#print(input.replace(old, new))
		return input.replace(old, new)

	for key, value in items:
		input[key] = update_info(value, old, new)

	return input



def generate_message(cases,case_id):

    msg_content = cases[case_id]["data"]
    body_file = open("body.html", "r")
    body = body_file.read().encode("utf-8")
    if body == "":
        message = msg_content["from_header"] + msg_content["to_header"] + msg_content["subject_header"] + msg_content["other_headers"] + msg_content["body"]
    else:
        message = msg_content["from_header"] + msg_content["to_header"] + msg_content["subject_header"] + msg_content["other_headers"] + body
        
    return message
    
		
def generate_smtp_seqs(cases):
    print("entrem aqui")
    case_id = cases["case_id"]

    smtp_seqs = {
        "helo": cases[case_id]["helo"],
        "mailfrom": cases[case_id]["mailfrom"],
        "rcptto": cases[case_id]["rcptto"],
        "msg_content": generate_message(cases,case_id)
    }
    print(smtp_seqs)
    return smtp_seqs
