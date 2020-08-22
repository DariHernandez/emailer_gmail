#!  python3
#   Access to gmail acount with selenium, and send email 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time, json

#Get password and email by file
fileUser = os.path.dirname (__file__) + '/user.json'
fileMails = os.path.dirname (__file__) + '/mails.json'

mailsInfo = []
userInfo = {} 

def capture_user_info (): 
    """ Input user information """
    mail = input("Not user file found. \nWhat is your gmail address? ")
    password = input("What is your password? ")
    info = {'mail': mail, 'password': password }
    return info

def capture_email_info (): 
    """ Input email information """
    mails = []

    while True: 
        addressee = input('\naddressee: ')
        subject = input('subject: ')
        body = input('body: ')
        otherMail = input ('\nother email (y/n) ')

        mail = {'addresse' : addressee, 'subject' : subject, 'body' : body}
        mails.append(mail)

        if otherMail == 'y': 
            continue
        else: 
            break

    return mails        


def open_json (file, write_menssage, read_menssage): 
    """ Open and read or write json file"""
    try:
        with open(file) as f_obj:
            print(read_menssage)
            return json.load(f_obj)
    except FileNotFoundError: 
        info = capture_user_info()

        with open(file, 'w') as f_obj:
            json.dump(info, f_obj)
            print(confim_menssage)

        return userInfo

"""
# Open USER file. If file dooesn't exist, make new file and store information
try:
    with open(fileMails) as f_obj:
        mailsInfo = json.load(f_obj)
except FileNotFoundError: 
    mails = []
    print ('\nNot mails file found. Register the mail information')

    while True: 
        addressee = input('\naddressee: ')
        subject = input('subject: ')
        body = input('body: ')
        otherMail = input ('\nother email (y/n) ')

        mail = {'addresse' : addressee, 'subject' : subject, 'body' : body}
        mails.append(mail)

        if otherMail == 'y': 
            continue
        else: 
            break        

    with open(fileMails, 'w') as f_obj:
        json.dump(mails, f_obj)
        print('Emails saved')
else:
    print('Sending emails...')

#Reed USER file information
with open(fileMails) as f_obj:
    mailsInfo = json.load(f_obj) 
"""

#Open browser
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

# Get user and information
userInfo = open_json (fileUser, 'Your email and password has been saved.', 'Reading user information')

my_user = userInfo['mail']
my_password = userInfo['password']

#Access to google/gmail acount and wait
google_access(my_user, my_password) 
time.sleep(3)

#Send mails
mailsInfo = open_json (fileMails, 'Emials information saved.', 'Reading mails information')
for mail in mailsInfo:
    send_mail (mail['addresse'], mail['subject'], mail['body'])
time.sleep(3)

#End and close
browser.close()
print ('Emails correct sent')

