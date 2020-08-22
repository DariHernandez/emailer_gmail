#!  python3
#   Access to gmail acount with selenium, and send email 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time, json

#Get password and email by file
file = os.path.dirname (__file__) + '/user.json'

userInfo = {} 

# Open user file. If file dooesn't exist, make new file and store information
try:
    with open(file) as f_obj:
        userInfo = json.load(f_obj)
except FileNotFoundError: 
    mail = input("What is your gmail address? ")
    password = input("What is your password? ")
    credential = {'mail': mail, 'password': password }
    with open(file, 'w') as f_obj:
        json.dump(credential, f_obj)
        print("We'll remember you when you come back, " + credential['mail'] + "!")
else:
    print("Welcome back, " + userInfo['mail'] + " seending emails...")

with open(file) as f_obj:
    userInfo = json.load(f_obj) 

my_user = userInfo['mail']
my_password = userInfo['password']

#Open browser and file password
browser = webdriver.Chrome()

def google_access (user, password): 
    #Home acount page
    browser.get(f'https://accounts.google.com/AccountChooser?service=mail&continue=https://mail.google.com/mail/')

    #Fill username and submit
    inputUser = browser.find_element_by_id ('identifierId')
    inputUser.send_keys(user)
    inputUser.send_keys(Keys.TAB)
    inputUser.send_keys(Keys.TAB)
    inputUser.send_keys(Keys.ENTER)

    #Fill pasword and send form
    inputPass = WebDriverWait (browser, 10).until(
            EC.element_to_be_clickable ((By.CSS_SELECTOR, '#password div div div input'))
        )
    inputPass.send_keys(password)
    inputPass.send_keys(Keys.TAB)
    inputPass.send_keys(Keys.TAB)
    inputPass.send_keys(Keys.ENTER)

    browser.refresh()
    browser.get('https://mail.google.com/mail/u/0/h/uk7zlfw6gykj/?zy=e&f=1')

def send_mail (to, subject, body, auto_send = True): 

    #Find and click redact mail button
    mailBtn = WebDriverWait (browser, 10).until(
            EC.element_to_be_clickable ((By.LINK_TEXT, 'Redactar correo'))
        )
    mailBtn.click()
    
    #Identify parts of mail
    toText = browser.find_element_by_css_selector ('textarea[name="to"]')
    subjectText = browser.find_element_by_css_selector('input[name="subject"]')
    bodyText = browser.find_element_by_css_selector('textarea[name="body"]') 
    sendBtn = browser.find_element_by_css_selector('input[value="Enviar"]')

    #Write information and auto send
    toText.send_keys(to)
    subjectText.send_keys(subject)
    bodyText.send_keys(body)
    if auto_send: 
        sendBtn.click()

google_access(my_user, my_password)
time.sleep(3)
send_mail ('hernandezdarifrancisco@gmail.com', 'email example', 'this is a email example eith selenium')
time.sleep(3)
browser.close()
print ('Emails correct sent')

