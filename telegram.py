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

        time.sleep(2)
        self.driver.find_element_by_css_selector('button.Button:nth-child(4)').click()

        code_input = WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_id('sign-in-code'))

        code = input('Enter the verification code sent to the Telegram app on your phone: ')
        code_input.send_keys(code)

        try:
            password_input = WebDriverWait(self.driver, 5).until(lambda s: s.find_element_by_id('sign-in-password'))

            password = getpass('Enter the 2FA password: ')
            password_input.send_keys(password)

            time.sleep(2)
            self.driver.find_element_by_css_selector('.Button').click()

        except TimeoutException:
            pass

        self.search_bar = WebDriverWait(self.driver, 10).until(lambda s: s.find_element_by_id('telegram-search-input'))

    def quit(self):
        print('Exiting...')
        self.driver.quit()
        exit()

if __name__ == '__main__':
    phone = input('Insert the phone number for logging in: ')
    t = TelegramAutomation(phone)

    t.quit()