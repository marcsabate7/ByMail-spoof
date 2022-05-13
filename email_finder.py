from typing import final
import requests
from taser import printx
import json
import time
import sys

api_keys = ["6d103ea6d5d7d4b0fe81ab23efbf6e79fb2189fe","9c4f2d7d18ecbc378147e5443f76422e50cd13bd","8f1558da76c8bf09a601b9327d09556f864f8880"]

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
}

API_ROOT = 'https://2.intelx.io'
API_KEY = 'df9c2b7e-408d-41e2-b924-8cc793cb1e79'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'

def findEmails(domain):
    emails_caught = []
    for key in api_keys:
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

def finishSearch(uuid):
    h = {'x-key': API_KEY, 'User-Agent': USER_AGENT}
    r = requests.get(API_ROOT + f'/intelligent/search/terminate?id={uuid}', headers=h)
    if(r.status_code == 200):
        return True
    else:
        return r.status_code

def startSearch(term, maxresults=100, buckets=[], timeout=5, datefrom="", dateto="", sort=4, media=0, terminate=[], target=0):
    h = {'x-key': API_KEY, 'User-Agent': USER_AGENT}
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

def getResults(id, limit=1000, offset=-1):
    h = {'x-key': API_KEY, 'User-Agent': USER_AGENT}
    r = requests.get(API_ROOT + f'/phonebook/search/result?id={id}&limit={limit}&offset={offset}', headers=h)
    if(r.status_code == 200):
        return r.json()
    else:
        return r.status_code

def queryResults(id, limit):
    results = getResults(id, limit)
    return results

def findMoreEmails(term, maxresults=1000, buckets=[], timeout=5, datefrom="", dateto="", sort=4, media=0, terminate=[], target=0):
    results = []
    results2 = []
    done = False
    search_id = startSearch(term, maxresults, buckets, timeout, datefrom, dateto, sort, media, terminate, target)
    if(len(str(search_id)) <= 3):
        done = True
    while done == False:
        time.sleep(1)  # lets give the backend a chance to aggregate our data
        r = queryResults(search_id, maxresults)
        results.append(r)
        maxresults -= len(r['selectors'])
        if(r['status'] == 1 or r['status'] == 2 or maxresults <= 0):
            if(maxresults <= 0):
                finishSearch(search_id)
            done = True
    print(results)
    all_emails = results[0]["selectors"]
    for email in all_emails:
        value = email["selectorvalue"]
        if len(value) > 25:
            break
        else:
            results2.append(value)
    return results2

def emailFinder(domain):
    printx.colored("\n[+] Searching emails for "+'\033[1m' + str(domain) + '\033[1m' +"...",fg="blue")
    first_list = findEmails(domain)
    second_list = findMoreEmails(domain)
    final_list = first_list + second_list
    printx.colored("[+] Treating data...",fg="blue")
    last_list = []

    for email in final_list:
        if email.find("@") != -1:
            if email.find("http") == -1:
                last_list.append(email)
    final_new_list = list(set(last_list))
    for email in final_new_list:
        print(email)
    printx.colored("\n[✔] Found "+'\033[1m' + str(len(final_new_list)) +" emails" '\033[1m' +"!!",fg="green")
