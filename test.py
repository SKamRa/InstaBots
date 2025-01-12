from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import re, requests, time, zipfile

from selenium.webdriver.common.proxy import *

import modules.config as config


sockets = []
r = requests.get("https://www.sslproxies.org/")
matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
revised_list = [m1.replace("<td>", "") for m1 in matches]
for socket_str in revised_list:
    if '-' in socket_str:
        continue
    
    socket_str = socket_str[:-5].replace("</td>", ":")
    #sockets.append((socket_str[:socket_str.find(':')], socket_str.split(':')[1]))
    port = socket_str.split(':')[1]
    if port == '80':
        sockets.append(socket_str)

PROXY = sockets[5]

PROXY_HOST = "38.154.227.167"
PROXY_PORT = "5868"
PROXY_USER = "nqpbrxmz"
PROXY_PASS = "16tlpokrb0lf" 
print(PROXY)
print(sockets)
    
chrome_options = webdriver.ChromeOptions()

service = Service(executable_path=config.Config["chromedriver_path"])

""" proxy without authentication
chrome_options.add_argument('--proxy-server=%s' % PROXY)
webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL",
}
webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True"""

manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

pluginfile = 'proxy_auth_plugin.zip'
with zipfile.ZipFile(pluginfile, 'w') as zp:
    zp.writestr("manifest.json", manifest_json)
    zp.writestr("background.js", background_js)
chrome_options.add_extension(pluginfile)

chrome = webdriver.Chrome(service=service, options=chrome_options)
chrome.get("http://whatismyip.com")

time.sleep(100)