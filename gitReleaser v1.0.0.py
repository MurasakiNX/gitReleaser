from requests import get, exceptions
from os import remove, mkdir
from os.path import exists, isfile, isdir
from time import sleep
from getpass import getuser
from datetime import datetime

token = ""

def human_size(bytes, units=[" bytes","KB","MB","GB","TB","PB","EB"]):
    return str(bytes) + units[0] if bytes < 1024 else human_size(bytes>>10, units[1:]) if units[1:] else f"{bytes>>10}ZB"

def setup():
    if exists("key.txt"):
        remove("key.txt")
    print("> Welcome to the configuration menu, for the software to work properly, you need your GitHub access token, to retrieve it please refer to the following help site: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token you will need to copy the generated token and put it below (Please uncheck all options when creating your token, gitReleaser doesn't need it).")
    token = input("\n> Enter your GitHub access token: ")
    while not checkKey(token):
        print("> The GitHub access token you specified is incorrect, please specify a correct one.")
        token = input("> Enter your GitHub access token: ")
    print("> Perfect! The access token that you specified is correct, and you can now access all the features of gitReleaser.")
    with open("key.txt", "w") as setup:
        setup.write(token)
    return token

def checkKey(key):
    if get("https://api.github.com/", headers={"Authorization": f"token {key}"}).headers["X-RateLimit-Limit"] == "60":
        return False
    return True

while True:
    try:
        print("""
       _ _  ______     _                          
      (_) | | ___ \   | |                         
  __ _ _| |_| |_/ /___| | ___  __ _ ___  ___ _ __ 
 / _` | | __|    // _ \ |/ _ \/ _` / __|/ _ \ '__|
| (_| | | |_| |\ \  __/ |  __/ (_| \__ \  __/ |   
 \__, |_|\__\_| \_\___|_|\___|\__,_|___/\___|_|   
  __/ |                                           
 |___/                    v1.0.0, by Murasaki#2936
    """)
        if token == "":
            if not exists("key.txt") or not isfile("key.txt"):
                print(f"> Welcome {getuser()} on gitReleaser ! We notice that you haven't configured the software yet. That's why you will be redirected to the configuration menu.\n")
                token = setup()
            else:
                with open("key.txt", "r") as key:
                    token = key.read()
                    if not checkKey(token):
                        print("> The token in the key.txt file is incorrect or no longer valid according to GitHub, so you will return to the configuration menu.\n")
                        token = setup()
        author = input("\n> Enter the repo author's name: ")
        name = input("> Enter the repo's name: ")

        request = get(f"https://api.github.com/repos/{author}/{name}/releases", headers={
            "Authorization": f"token {token}"
        })

        reset = datetime.fromtimestamp(int(request.headers["x-ratelimit-reset"])).strftime("%H:%M:%S %p")

        if int(request.headers["x-ratelimit-remaining"]) == 0:
            print(f"> You can no longer use this key to retrieve GitHub rests because you have exceeded the number of uses per hour, you must wait {reset} to use it again.")
        elif int(request.headers['x-ratelimit-limit']) == 60:
            print("> The token in the key.txt file is incorrect or no longer valid according to GitHub, so you will return to the configuration menu.\n")
            token = setup()
        else:
            if request.status_code == 404:
                print("> No GitHub repo has been found with this name and this author.")
            else:
                latest = request.json()[0]
                if not latest["assets"]:
                    print("> This GitHub repo doesn't contain any files, so you can't continue.")
                else:
                    assets = latest["assets"]
                    choose = input(f"> Do you really want to download the latest update of this GitHub repo? [Y/n] ")
                    
                    if choose.upper() == "N" or choose.upper() != "Y" and choose.upper() != "":
                        print("> The download of this GitHub repo has been cancelled.")
                    elif choose.upper() == "Y" or choose.upper() == "":
                        if not exists(name) or not isdir(name):
                            mkdir(name)
                        for asset in assets:
                            download = input(f"> Do you want to download {asset['name']} [{human_size(asset['size'])}]? [Y/n] ")
                            if download.upper() == "N" or download.upper() != "Y" and download.upper() != "":
                                continue
                            else:
                                file = get(asset["browser_download_url"])
                                with open(f"{name}/{asset['name']}", "wb") as f:
                                    f.write(file.content)
                                print(f'> {asset["name"]} has been downloaded!')
                        print("> All desired files have been downloaded!")
    except KeyboardInterrupt:
        print("\n> You have decided to leave gitReleaser.")
        break
    except exceptions.ConnectionError:
        print("> Please check that you are connected to the Internet.")
    except exceptions.Timeout:
        print("> gitReleaser took too long to get a response from GitHub.")
    except exceptions.RequestException as e:
        print(f"> An error occured, please report Murasaki#2936 on Discord, or on the Issue tab of gitReleaser. Error information is available in the error.txt file.")
        with open('error.txt', 'w') as errfile:
            errfile.write(e)
    except:
        print("> An error has occurred, please check that you are connected to the Internet.")
        break    
sleep(2)
