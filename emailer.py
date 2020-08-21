#!  python3
#   Access to gmail acount with selenium, and send email 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os


my_user = 'cidentymx@gmail.com'
my_password = 'duscordia de ceguera temporal 87'


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
send_mail ('hernandezdarifrancisco@gmail.com', 'email example', 'this is a email example eith selenium')


