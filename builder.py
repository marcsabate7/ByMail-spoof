from additional.common import *
import sys

class Builder(object):

	def __init__(self, cases, config,victim_email,last_victim_email):
		self.config = config
		self.case_id = config["case_id"].decode("utf-8")
		self.victim_email = victim_email.encode("utf-8")
		self.last_victim_email = last_victim_email.encode("utf-8")
		self.update_rcptto_info(cases,self.last_victim_email)
		self.cases = self.update_cases_info(cases,self.victim_email)


	def update_cases_info(self,cases, victim_email):
		cases = update_info(cases, b"attack.com", self.config["attacker_site"])
		cases = update_info(cases, b"admin@legitimate.com", self.config["legitimate_site_address"])
		legitimate_site = self.config["legitimate_site_address"].split(b"@")[1]
		cases = update_info(cases, b"legitimate.com", legitimate_site)
		cases = update_info(cases, b"victim@victim.com", victim_email)

		#print(cases)
		return cases


	def update_rcptto_info(self,cases, last_victim_email):
		cases = update_info(cases, last_victim_email, b"victim@victim.com")


	def generate_message(self):
		cases = self.cases
		case_id = self.case_id
		msg_content = cases[case_id]["data"]
		body_file = open("body.html", "r")
		body = body_file.read().encode("utf-8")
		if body == "":
			message = msg_content["from_header"] + msg_content["to_header"] + msg_content["subject_header"] + msg_content["other_headers"] + msg_content["body"]
		else:
			message = msg_content["from_header"] + msg_content["to_header"] + msg_content["subject_header"] + msg_content["other_headers"] + body

		return message
		
		
	def generate_smtp_seqs(self):
		cases = self.cases
		case_id = self.case_id

		smtp_seqs = {
			"helo": cases[case_id]["helo"],
			"mailfrom": cases[case_id]["mailfrom"],
			"rcptto": cases[case_id]["rcptto"],
			"msg_content": self.generate_message()
		}

		#print(smtp_seqs)
		return smtp_seqs
