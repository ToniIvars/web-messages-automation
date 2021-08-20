from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import time
from getpass import getpass

class UsernameError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class MessageError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InstagramAutomation:
    def __init__(self, username, password):
        opt = Options()
        opt.add_argument('--headless')

        self.driver = webdriver.Firefox(options=opt)
        self.driver.get('https://www.instagram.com/accounts/login')

        WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_css_selector('button.aOOlW.bIiDR')).click()

        username_input = WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_name('username'))
        username_input.send_keys(username)

        password_input = WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_name('password'))
        password_input.send_keys(password)

        try:
            WebDriverWait(self.driver, 5).until_not(lambda s: s.find_element_by_class_name('pbNvD'))
            self.driver.find_element_by_class_name('L3NKy').click()
        except TimeoutException:
            print('There was an error')
            self.quit()

        WebDriverWait(self.driver, 10).until(lambda s: s.find_element_by_class_name('xWeGp')).click()

        WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_css_selector('button.aOOlW:nth-child(2)')).click()

        self.new_message_btn = self.driver.find_element_by_class_name('wpO6b')

    def change_recipient(self, username):
        if not username:
            raise UsernameError('You have to enter a name')

        self.new_message_btn.click()
        time.sleep(0.2)
        self.driver.find_element_by_class_name('j_2Hd').send_keys(username)

        try:
            WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_class_name('_3wFWr'))
        except TimeoutException:
            raise UsernameError('Name not found')

        WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_css_selector('div.-qQT3:nth-child(1)')).click()
        self.driver.find_element_by_css_selector('div.WaOAr:nth-child(3) > div:nth-child(1)').click()

        self.message_input = WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_css_selector('.ItkAi > textarea:nth-child(1)'))

        recipient = self.driver.find_element_by_css_selector('._56XdI > div:nth-child(1) > div:nth-child(1)')
        return f'Recipient changed to: {recipient.text}'

    def send_message(self, message, times=1):
        if not message:
            raise MessageError('You have to enter a message')
        if times < 1:
            raise MessageError('The minimum times are 1')

        self.message_input.send_keys(message)
        time.sleep(0.2)

        self.driver.find_element_by_css_selector('div.JI_ht:nth-child(3) > button:nth-child(1)').click()

        return f'Message sent {times} times'
    
    def send_messages(self, messages):
        if not messages or len(messages) < 2:
            raise MessageError('You have to enter 2 or more messages')

        for message in messages:
            self.message_input.send_keys(message)
            time.sleep(0.2)

            self.driver.find_element_by_css_selector('div.JI_ht:nth-child(3) > button:nth-child(1)').click()

        return f'{len(messages)} messages sent'

    def quit(self):
        print('Exiting...')
        self.driver.quit()
        exit()

if __name__ == '__main__':
    username = input('Username or email: ')
    password = getpass('Password:')

    i = InstagramAutomation(username, password)

    recipient = input('Username of the recipient of the message: ')
    print(i.change_recipient(recipient))

    message = input('Message: ')
    print(i.send_message(message))

    i.quit()