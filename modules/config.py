import os.path
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_DIR = os.path.join(BASE_DIR, 'Assets' )

Config = {
    "bot_type" : 0, #change to 2 to use python requests
    "chromedriver_path": f"{BASE_DIR}\\ressources\\drivers\\chromedriver\\chromedriver.exe",  # if windows 'chromedriver.exe'
    "chromedriver_captcha_ext": f"{BASE_DIR}\\ressources\\captcha\\plugin\\Buster\\Buster-Captcha-Solver-for-Humans.crx",
    "chromedriver_xpath_ext": f"{BASE_DIR}\\xPath-Finder.crx",
    "use_custom_proxy" : False, #default is False change to True to use a file containing multiple proxies of yours.
    "use_local_ip_address" : True, #default is False chnage to True to user your computers ip directly.
    "amount_of_account": 1, #amount of account you want to create make sure it doesnt exceed 50 for better performance
    "amount_per_proxy": 1, #this would be amont of account used if you have a you are using multiple proxies
    "proxy_file_path" : ASSET_DIR + "/proxies.txt",
    "email_domain": "gmail.com",
    "country": "it",
    "activation_email_addr": "xxxxxxxxxxxxxxxx",
    "activation_email_pass": "xxxxxxxxxxxxxxxx",
    "activation_email_serv": "xxxxxxxxxxxxxxxx",
    "activation_email_spor": 993,
}