from time import sleep 
import random
import datetime
import re

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common import NoSuchElementException, InvalidSelectorException

import modules.config as config

from modules.creator import createPassword
from modules.creator import createFullname
from modules.conntest import *
from modules.db import log_new_account


class InstaBots:
    def __init__(self):
        service = Service(executable_path=config.Config["chromedriver_path"])
        op = Options()
        op.add_extension(config.Config['chromedriver_captcha_ext'])
        op.add_extension(config.Config['chromedriver_xpath_ext'])
        # Adding argument to disable the AutomationControlled flag 
        op.add_argument("--disable-blink-features=AutomationControlled") 
        # Exclude the collection of enable-automation switches
        op.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        # Turn-off userAutomationExtension 
        op.add_experimental_option("useAutomationExtension", False)

        self.proxys = []
        self.__collect_sockets()
        print(self.proxys)
        self.proxy_host = self.proxys[0][0]
        self.proxy_port =self.proxys[0][1]

        try:
            self.driver = webdriver.Chrome(service=service, options=op)
            self.driver.delete_all_cookies()
            # Changing the property of the navigator value for webdriver to undefined 
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
            self.action_chains = ActionChains(self.driver)
        except DeprecationWarning:
            pass
        
        self.driver.maximize_window()

    def __collect_sockets(self):
        r = requests.get("https://www.sslproxies.org/")
        matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
        revised_list = [m1.replace("<td>", "") for m1 in matches]
        for socket_str in revised_list:
            self.proxys.append(socket_str[:-5].replace("</td>", ":"))
            

    def getEmail(self):
        if self.reset:
            self.driver.get("https://tempail.com/fr")
            sleep(6)
            
        try:
            solver_button = self.driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[4]")
            print("captcha1")
            solver_button = self.driver.find_element(By.ID, "solver-button")
            print("captcha2")
            solver_button.click()
            print("Bypassing captcha")
        except (InvalidSelectorException, NoSuchElementException):
            pass
        """try:
            cookies_win = self.driver.find_element(By.CLASS_NAME, "fc-consent-root")
            self.driver.find_element(By.CLASS_NAME, "fc-cta-do-not-consent").click()
        except:
            pass
        """
        
        sleep(self.conn_delay + 2)
        
        #do_not_consent_cookies 
        self.driver.find_element(By.XPATH, "//p[@class and text()='Do not consent']").click()

        try:
            email_element = self.driver.find_element(By.ID, "eposta_adres")
        except (NoSuchElementException, InvalidSelectorException):
            sleep(self.conn_delay + 2)
            self.getEmail()

        searching = True
        while searching:
            try:
                self.email = email_element.get_attribute("value")
                searching = False
            except Exception as e:
                print(f"[-] An error occured : {e}")
                

    def setBirthday(self):
        possible_ranges = [12, 28, 50]
        all_options = self.driver.find_elements(By.CLASS_NAME, "_aau-")
        choices = []

        print(2)

        for i in range(3):
            if i == 2:
                option_visible_num = datetime.date.today().year - random.randint(18, possible_ranges[i])
            else:
                option_visible_num = random.randint(1, possible_ranges[i])

            sel = Select(all_options[i])
            sel.select_by_value(value=str(option_visible_num))
            #self.driver.execute_script("for(var j = 0; j < 3; j++){ var select = document.getElementsByClassName('_aau-')[j]; for(var i = 0; i < select.options.length; i++){ if(i == arguments[0]){ select.options[i].selected = true; } }}", option_visible_num);
            choices.append(option_visible_num)
            print(f"Option {i} selected : {option_visible_num}")
            sleep(random.randint(3, 6))

        print("[+] Birthday : ",end='')
        for date in range(len(choices)):
            print(choices[date],end='')
            if date != 2:
                print("/",end='')

        sleep(1)
        submit = self.driver.find_element(By.XPATH, "//button[text()='Suivant']")
        self.action_chains.move_to_element(submit)
        sleep(1)
        submit.click()
        sleep(2)
        

    def set_email_confirmation_code(self, code):
        self.driver.switch_to.window(self.driver.window_handles[1])
        sleep(self.conn_delay)
        field = self.driver.find_element(By.XPATH, "//input[@name='email_confirmation_code']")
        field.clear()
        field.send_keys(code)
        sleep(1)

        submit = self.driver.find_element(By.XPATH, "//div[@role='button' and text()='Suivant']")
        self.action_chains.move_to_element(submit)
        submit.click()
        sleep(3)
        

    def fetch_email_confirmation_code(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        sleep(10)

        searching = True
        i = 0
        while searching and i < 20:
            verification_code_field = self.driver.find_elements(By.CLASS_NAME, "baslik")[-1]
            if "instagram" in verification_code_field.text.lower():
                searching = False
                code_without_filtering = verification_code_field.text
                code = code_without_filtering.strip().split(" ")[0]
                print(f"[+] Verification code : {code}")
                return code

            i += 1
            sleep(5)

        raise "[-] Error : cannot get the verification code\nExit"
    
    
    def createInstaBot(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("https://www.instagram.com/accounts/emailsignup/")

        sleep(5)
        
        # refusing the non-essential cookies
        try:
            self.driver.find_element(By.CLASS_NAME, '_a9_1').click()
        except (NoSuchElementException, InvalidSelectorException):
            pass
        
        sleep(7)

        # fetching the account infos
        self.fullname = createFullname()
        self.password = createPassword()
        self.username = self.email[:self.email.find("@")]
        
        fields = ['emailOrPhone', 'fullName', 'username', 'password']
        creds = [self.email, self.fullname, self.username, self.password]

        # filling the fields
        i = 0
        for fielditem in fields:
            field = self.driver.find_element(By.NAME, fielditem)
            self.action_chains.move_to_element(field)
            field.clear()
            
            for letter in creds[i]:
                field.send_keys(letter)
                randomsleep = random.randint(5, 50)
                sleep(randomsleep/100)
            i += 1
            sleep(2)
            
        sleep(1)

        submit = self.driver.find_element(By.XPATH, "//button[@type='submit' and text()='Suivant']")
        self.action_chains.move_to_element(submit)
        sleep(2)
        submit.click()
        sleep(3)

        try:
            if self.driver.find_element(By.XPATH, "//div[@class='_aaht']//p[@id='ssfErrorAlert']"):
                sleep(2)
                self.driver.close()
                sleep(0.2)
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.reset = False
                sleep(11)
                self.request()
        except NoSuchElementException:
            pass

        self.setBirthday()
        sleep(1)
        email_confirmation_code = self.fetch_email_confirmation_code()
        self.set_email_confirmation_code(email_confirmation_code)
        
        i = 0
        searching = True
        while searching and i < 40:
            try:
                if self.driver.find_element(By.XPATH, "//span[text()='Impossible de créer votre compte. Veuillez réessayer dans quelques instants.']"):
                    print("[-] Impossible to create an account.\nRetrying. . .")
                    searching = False
                    self.driver.delete_all_cookies()
                    self.driver.close()
                    self.main()
            except:
                i += 1
            sleep(1)

    def check_if_success(self):
        sleep(10)

        # searching for 40 seconds
        i = 0
        searching = True
        while searching and i < 40:
            try:
                if self.driver.find_element(By.XPATH, "//span[text()='L\'adresse IP que vous utilisez a été signalée comme un proxy ouvert. Si vous pensez qu\'il s\'agit d\'une erreur, rendez-vous sur http://help.instagram.com/']") \
                or self.driver.find_element(By.XPATH, "//span[text()='Impossible de créer votre compte. Veuillez réessayer dans quelques instants.']"):
                    self.proxy_host = self.proxys[self.proxys.index(self.proxy_host) + 1][0]
                    self.proxy_port = self.proxys[self.proxys.index(self.proxy_host) + 1][1]
                    
                    return False
                if self.driver.find_element(By.XPATH, "//span[text()='Suggestions pour vous']"):
                    searching = False
                    return True
            except:
                i += 1
            sleep(1)
        return False


    def main(self):
        self.conn_delay = connectionTest()
        print(f"[@] Test success : {round(self.conn_delay*1000)} ms\n")

        self.reset = True
        self.getEmail()
        self.createInstaBot()
        if self.check_if_success():
           log_new_account.new(fullname=self.fullname, email=self.email, username=self.username, password=self.password)
           print(f"[+] New account logged!\n{self.fullname} | {self.username} | {self.password}\n")

        self.driver.close()


if __name__ == '__main__':
    instabot = InstaBots()
    instabot.main()