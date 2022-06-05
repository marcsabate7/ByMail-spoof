from taser import printx
import dns
from tqdm import tqdm
import sys
import requests
import socket
from tabulate import tabulate

def add(domain):
		return [domain + chr(i) for i in (*range(48, 58), *range(97, 123))]

def bitChanger(domain):
	list = []
	masks = [1, 2, 4, 8, 16, 32, 64, 128]
	chars = set('abcdefghijklmnopqrstuvwxyz0123456789-')
	for i, c in enumerate(domain):
		for mask in masks:
			b = chr(ord(c) ^ mask)
			if b in chars:
				list.append(domain[:i] + b + domain[i+1:])
	return list

def bithype(domain):
	return [domain[:i] + '-' + domain[i:] for i in range(1, len(domain))]

def bitInsertion(domain):
	result = set()
	for i in range(1, len(domain)-1):
		prefix, orig_c, suffix = domain[:i], domain[i], domain[i+1:]
		for c in (c for keys in keyboards for c in keys.get(orig_c, [])):
			result.update({
				prefix + c + orig_c + suffix,
				prefix + orig_c + c + suffix
			})
	return result

def bitOmit(domain):
	return [domain[:i] + domain[i+1:] for i in range(len(domain))]

def bitRepeat(domain):
	return [domain[:i] + c + domain[i:] for i, c in enumerate(domain)]

def bitReplacement(domain):
	list = []
	for i, c in enumerate(domain):
		pre = domain[:i]
		suf = domain[i+1:]
		for layout in keyboards:
			for r in layout.get(c, ''):
				list.append(pre + r + suf)
	return list

def transposition(domain):
	return [domain[:i] + domain[i+1] + domain[i] + domain[i+2:] for i in range(len(domain)-1)]

def vowelSwepper(domain):
	list = []
	vowels = 'aeiou'
	for i in range(0, len(domain)):
		for vowel in vowels:
			if domain[i] in vowels:
				list.append(domain[:i] + vowel + domain[i+1:])
	return list

def iSwepper(domain):
	list = []
	vowels = 'i'
	for i in range(0, len(domain)):
		if domain[i] in vowels:
			list.append(domain[:i] + 'l' + domain[i+1:])
	return list

def lSwepper(domain):
	list = []
	vowels = 'l'
	for i in range(0, len(domain)):
		if domain[i] in vowels:
			list.append(domain[:i] + 'i' + domain[i+1:])
	return list

qwerty = {
	'1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7yt5', '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
	'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6ygfr5', 'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
	'a': 'qwsz', 's': 'edxzaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft', 'h': 'ujnbgy', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
	'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
	}
qwertz = {
	'1': '2q', '2': '3wq1', '3': '4ew2', '4': '5re3', '5': '6tr4', '6': '7zt5', '7': '8uz6', '8': '9iu7', '9': '0oi8', '0': 'po9',
	'q': '12wa', 'w': '3esaq2', 'e': '4rdsw3', 'r': '5tfde4', 't': '6zgfr5', 'z': '7uhgt6', 'u': '8ijhz7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0',
	'a': 'qwsy', 's': 'edxyaw', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'zhbvft', 'h': 'ujnbgz', 'j': 'ikmnhu', 'k': 'olmji', 'l': 'kop',
	'y': 'asx', 'x': 'ysdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
	}
azerty = {
	'1': '2a', '2': '3za1', '3': '4ez2', '4': '5re3', '5': '6tr4', '6': '7yt5', '7': '8uy6', '8': '9iu7', '9': '0oi8', '0': 'po9',
	'a': '2zq1', 'z': '3esqa2', 'e': '4rdsz3', 'r': '5tfde4', 't': '6ygfr5', 'y': '7uhgt6', 'u': '8ijhy7', 'i': '9okju8', 'o': '0plki9', 'p': 'lo0m',
	'q': 'zswa', 's': 'edxwqz', 'd': 'rfcxse', 'f': 'tgvcdr', 'g': 'yhbvft', 'h': 'ujnbgy', 'j': 'iknhu', 'k': 'olji', 'l': 'kopm', 'm': 'lp',
	'w': 'sxq', 'x': 'wsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhj'
	}
keyboards = [qwerty, qwertz, azerty]



def checkIfDomainExists(domain):
	try:
		result = socket.gethostbyname(domain)
		return True
	except:
		printx.colored("[✖] This domain doesn't exist!", fg="red")
		result = input("-> You want to proceed? (Y/N): ")
		if result == "Y" or result == "y" or result == "YES" or result == "yes" or result == "Yes":
			return True
		else:
			return False



def sameDomain(domain):
	existance = checkIfDomainExists(domain)
	if existance == True:
		printx.colored("\n[+] Generating similar domains for "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
		partial_domain = domain.split(".",1)
		first_part_domain = partial_domain[0]
		f = add(first_part_domain)
		f2 = bitChanger(first_part_domain)
		f3 = bithype(first_part_domain)
		f4 = bitInsertion(first_part_domain)
		f5 = bitOmit(first_part_domain)
		f6 = bitRepeat(first_part_domain)
		f7 = bitReplacement(first_part_domain)
		f8 = transposition(first_part_domain)
		f9 = vowelSwepper(first_part_domain)
		f10 = iSwepper(first_part_domain)
		f11 = lSwepper(first_part_domain)
		final_list = list(f) + list(f2) + list(f3) + list(f4) + list(f5) + list(f6) + list(f7) + list(f8) + list(f9) + list(f10) + list(f11)
		new_final_list = list(set(final_list))
		new_final_list2 = []
		for elem in new_final_list:
			elem = elem + "."+partial_domain[1]
			new_final_list2.append(elem)
		printx.colored("[✔] Domains generated, checking availavility...\n ",fg="green")
		complete_list = []
		for i in tqdm(range(len(new_final_list2))):
			try:
				result = ""
				result2 = dns.resolver.resolve(new_final_list2[i], 'A')
				answers = dns.resolver.query(new_final_list2[i], 'MX')
				if len(answers) !=0:
					for answer in answers:
						data = str(answer)
						data = data.split(" ")
						if result == "":
							result = data[1]
						else: 
							result = result + " / " + data[1]
			except:
				result = "\033[1;32;40mAVAILABLE!\033[0m"
			complete_list.append([new_final_list2[i], result])
		print("\n")
		col_names = ["DOMAIN", "AVAILABILITY"]
		print(tabulate(complete_list, headers=col_names))
		print("\n\n")


