from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import time

class MessageError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UsernameError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class WhatsappAutomation:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.get(f'https://web.whatsapp.com/')

        print('Read the QR code with your phone, please (this will only occur once).')
        try:           
            WebDriverWait(self.driver, 20).until(lambda s:s.find_element_by_id('side'))
            self.driver.minimize_window()

        except TimeoutException:
            print('You have 20 seconds to read the QR code.')
            self.quit()

        try:
            self.search_bar = WebDriverWait(self.driver, 10).until(lambda s:s.find_element_by_class_name('_13NKt'))

        except TimeoutException:
            print('An error occurred')
            self.quit()
    
    def change_recipient(self, name):
        if not name:
            self.driver.quit()
            raise UsernameError('You have to enter a name')

        self.search_bar.click()
        time.sleep(0.5)
        self.search_bar.send_keys(name)

        try:
            WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_class_name('i0jNr'))
            self.driver.quit()
            raise UsernameError('Name not found')
        except TimeoutException:
            pass

        self.search_bar.send_keys(Keys.ENTER)

        self.inp = self.driver.find_element_by_css_selector('._1LbR4 > div:nth-child(2)')

        recipient = self.driver.find_element_by_css_selector('._21nHd > span:nth-child(1)')

        return f'Recipient changed to: {recipient.text}'

    def send_message(self, message, times=1):
        if not message:
            self.driver.quit()
            raise MessageError('You have to write a message')
        if times < 1:
            self.driver.quit()
            raise MessageError('You cannot send a message less than 1 time')

        for _ in range(times):
            self.inp.send_keys(message + Keys.ENTER)
            time.sleep(0.5)

        return f'Message sent successfully {times} time{"s" if times > 1 else ""}'

    def send_messages(self, messages_list):
        if not messages_list or len(messages_list) < 2:
            self.driver.quit()
            raise MessageError('You have to pass a list of messages')

        for message in messages_list:
            self.inp.send_keys(message + Keys.ENTER)
            time.sleep(0.5)

        return f'{len(messages_list)} messages sent successfully'

    def quit(self):
        print('Exiting...')
        self.driver.quit()
        exit()

if __name__ == '__main__':
    w = WhatsappAutomation()

    recipient = input('Recipient of the message: ')
    print(w.change_recipient(recipient))

    message = input('Insert the message you want to send: ')
    print('\n' + w.send_message(message))

    w.quit()