from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import time
from getpass import getpass

class TelegramAutomation:
    def __init__(self, phone):
        opt = Options()
        opt.add_argument('--headless')

        self.driver = webdriver.Firefox(options=opt)
        self.driver.get('https://web.telegram.org/z/')

        WebDriverWait(self.driver, 20).until(lambda s: s.find_element_by_css_selector('button.Button:nth-child(5)'))
        self.driver.find_element_by_css_selector('button.Button:nth-child(4)').click()

        phone_input = WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_id('sign-in-phone-number'))

        if not '34' in phone_input.get_attribute('value'):
            phone_input.send_keys('+34' + phone)
        else:
            phone_input.send_keys(phone)

        time.sleep(1)
        self.driver.find_element_by_css_selector('button.Button:nth-child(4)').click()

        try:
            code_input = WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_id('sign-in-code'))
        except TimeoutException:
            try:
                self.driver.find_element_by_class_name('error')
                print('There was an error with the phone.')
            except:
                print('There was an unknown error.')
            finally:
                self.quit()

        while True:
            code = input('Enter the verification code sent to the Telegram app on your phone: ')
            code_input.send_keys(code)

            try:
                WebDriverWait(self.driver, 2).until(lambda s: s.find_element_by_class_name('error'))
                print('The code is incorrect.')
                code_input.clear()

            except TimeoutException:
                break

        try:
            password_input = WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_id('sign-in-password'))

            while True:
                password = getpass('Enter the 2FA password: ')
                password_input.send_keys(password)

                time.sleep(1)
                self.driver.find_element_by_css_selector('.Button').click()

                try:
                    WebDriverWait(self.driver, 2).until(lambda s: s.find_element_by_class_name('error'))
                    print('The password is incorrect.')
                    password_input.clear()

                except TimeoutException:
                    break

        except TimeoutException:
            pass

        self.search_bar = WebDriverWait(self.driver, 10).until(lambda s: s.find_element_by_id('telegram-search-input'))

    def change_recipient(self, name):
        if not name:
            return 'You have to enter a name'

        self.search_bar.click()
        time.sleep(1)
        self.search_bar.send_keys(name)

        try:
            WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_class_name('search-section'))
        except TimeoutException:
            return 'Name not found'

        self.search_bar.send_keys(Keys.ENTER)

        recipient = self.driver.find_element_by_css_selector('.chat-info-wrapper > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > h3:nth-child(1)')
        return f'Recipient changed to: {recipient.text}'

    def send_message(self, message, times=1):
        if not message:
            return 'You have to enter a message'
        if times < 1:
            return 'The minimum times are 1'

        inp = self.driver.find_element_by_id('editable-message-text')

        for _ in range(times):
            inp.send_keys(message + Keys.ENTER)
            time.sleep(0.5)

        return f'Message sent {times} times'
    
    def send_messages(self, messages):
        if not messages or len(messages) < 2:
            return 'You have to enter 2 or more messages'

        inp = self.driver.find_element_by_id('editable-message-text')

        for message in messages:
            inp.send_keys(message + Keys.ENTER)
            time.sleep(0.5)

        return f'{len(messages)} messages sent'

    def quit(self):
        print('Exiting...')
        self.driver.quit()
        exit()

if __name__ == '__main__':
    phone = input('Insert the phone number for logging in: ')
    t = TelegramAutomation(phone)

    recipient = input('Recipient of the message: ')
    print(t.change_recipient(recipient))

    t.quit()