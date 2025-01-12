import sys
import time
import requests
 
def connectionTest():
    print("\n[*] Testing your connection")
    t0 = time.time()
    try:
        requests.get("https://google.com/")
    except ConnectionError:
        print("[ERROR] Connect to the internet")
        sys.exit()
    t1 = time.time()
    conn_delay = t1 - t0
    
    return conn_delay