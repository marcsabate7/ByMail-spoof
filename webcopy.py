from pywebcopy import save_website
from taser import printx
import time 
import requests

def websiteCopier(website_url):
    counter = 0

    while True:
        if counter == 3:
            printx.colored("[-] Maxium intents exceeded, we can't clone this website. Try with HTTrack!\n\n",fg="red")
            time.sleep(3)
            break
        try:
            print("\n")
            print("Note that if the website is to huge this can take some time...")
            printx.colored("[+] Starting cloning the website, please wait...",fg="blue")
            save_website(
                url=website_url,
                project_folder="./",
                project_name="my_site",
                bypass_robots=True,
                debug=False,
                open_in_browser=True,
                delay=None,
                threaded=False,
            )
            print("\n")
            printx.colored("[+] Website cloned succesfully:\n    - Saved in: ./my_site\n[✔] Browser opened with the cloned website!\n",fg="green")
            print("[!] If the website contains too JavaScript elements try with HTTrack for better performance!\n")
            break
        except:
            printx.colored("[-] An error has ocurred when clonning the website, retrying...",fg="red")
            counter+=1

