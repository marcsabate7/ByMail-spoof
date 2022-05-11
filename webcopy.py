from pywebcopy import save_website
from taser import printx

def websiteCopier(website_url):
    counter = 0
    while True:
        if counter == 3:
            printx.colored("Maxium intents exceeded, we can't clone this website. Try with HTTrack!\n\n",fg="red")
            break
        try:
            print("\n")
            print("Note that if the website is to huge this can take some time...")
            print("Starting cloning the website, please wait...")
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
            printx.colored("Website cloned succesfully, check 'my-site' folder and also the browser opened!\n\n",fg="green")
            break
        except:
            printx.colored("An error has ocurred when clonning the website, retrying...",fg="red")
            counter+=1

