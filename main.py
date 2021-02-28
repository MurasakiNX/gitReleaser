from requests import get, exceptions
from os import path, remove, system
from time import sleep

bakToken = ''
token = ''

def checkKey(key):
    if get('https://api.github.com/', headers={'Authorization': f'token {key}'}).headers['X-RateLimit-Limit'] == '60':
        return False
    return True

def setup():
    if path.exists('key.txt') and path.isdir('key.txt'):
        remove('key.txt')
    token = input('Your GitHub token: ')
    isValid = checkKey(token)
    while not isValid:
        print('This token is invalid !')
        token = input('Your GitHub token: ')
        isValid = checkKey(token)
    with open('key.txt', 'w') as setup:
        setup.write(token)

while True:
    system('clear')
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

    try:
        if not path.exists('key.txt') or not path.isfile('key.txt'):
            print('Welcome to gitReleaser\nTo get started please provide your GitHub token, if you don\'t know how to do this here\'s a link: https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token WARNING: Please uncheck all the boxes to just have a token without privileges, gitReleaser doesn\'t need it.')
            setup()
            print('Your GitHub token is valid, the setup process is over.\n')
        with open('key.txt', 'r') as file:
            token = file.read()
            if token != bakToken and not checkKey(token):
                print('The token in the key.txt file is incorrect !')
                setup()
            else:
                author = input('Enter the repo author\'s name: ')
                name = input('Enter the repo\'s name: ')

                request = get(f'https://api.github.com/repos/{author}/{name}/releases', headers={
                    'Authorization': f'token {token}'
                }).json()[0]

                assets = request['assets']

                for asset in assets:
                    file = get(asset['browser_download_url'])
                    with open(asset['name'], 'wb') as f:
                        f.write(file.content)
                    print(f'The file {asset["name"]} has just been downloaded !')
                print('All files have been downloaded !')
                bakToken = token

    except exceptions.ConnectionError:
        print('You must be connected to the Internet !')
        break
    except exceptions.Timeout:
        print('The program takes too long to access GitHub.')
        break
    except KeyboardInterrupt:
        print('\nYou have decided to leave the program.')
        break
    except:
        print('An error has occured !')
        break
sleep(2)
exit()
