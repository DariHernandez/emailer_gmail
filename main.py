#!  python3
#   Access to gmail acount with selenium, and send email 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rwJsonFile import readJsonFile, writeJsonFile
import os, time

#Get files information
fileUser = os.path.join(os.path.dirname (__file__), 'user.json')
fileMails = os.path.join(os.path.dirname (__file__), 'mails.json')

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

def open_json (file, typeInfo, write_menssage, read_menssage): 
    """Get information from the json files"""
    print(read_menssage)
    info = readJsonFile(file)
    if not info: 
        if typeInfo == 'user': 
            print ('Type your gmail info')
            info = capture_user_info()
        elif typeInfo == 'mail': 
            print ('Type the emails info')
            info = capture_email_info()
        writeJsonFile (file, info)
        print (write_menssage)
    return info

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

#Open browser
print ('Open Browser')
browser = webdriver.Chrome()

# Get user and information
userInfo = open_json (fileUser, 'user', 'Your email and password has been saved.', 'Reading user information')

my_user = userInfo['mail']
my_password = userInfo['password']

#Access to google/gmail acount and wait
print ('Loggin')
google_access(my_user, my_password) 
time.sleep(3)

#Send mails
mailsInfo = open_json (fileMails, 'mail', 'Emials information saved.', 'Reading mails information')
for mail in mailsInfo:
    print ('Sending email to %s' % (mail['addresse']))
    send_mail (mail['addresse'], mail['subject'], mail['body'])
time.sleep(3)

#End and close
browser.close()
print ('Emails correct sent')

