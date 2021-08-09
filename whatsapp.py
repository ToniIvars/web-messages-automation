from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import phonenumbers
import time

class InvalidPhoneError(Exception):
    def __init__(self):
        self.message = 'The phone number is invalid'
        super().__init__(self.message)

class WhatsappAutomation:
    def __init__(self, phone):
        try:
            parsed_phone = phonenumbers.parse(phone, 'ES')
            if not phonenumbers.is_valid_number(parsed_phone):
                raise InvalidPhoneError
        except:
            raise InvalidPhoneError

        self.driver = webdriver.Firefox()
        self.driver.get(f'https://web.whatsapp.com/send?phone={phone}')

        print('Read the QR code with your phone, please (this will only occur once).')
        try:
            WebDriverWait(self.driver, 20).until(lambda s:s.find_element_by_id('side'))
            self.driver.minimize_window()

            self.inp = WebDriverWait(self.driver, 10).until(lambda s:s.find_element_by_css_selector('._1LbR4 > div:nth-child(2)'))

        except TimeoutException:
            self.quit()
            print('You have 20 seconds to read the QR code.')

    def one_message(self, message, times=1):
        if not message:
            return 'Write a message'
        if times < 1:
            return 'You cannot send a messages less than 1 time'

        for _ in range(times):
            self.inp.send_keys(message + Keys.ENTER)
            time.sleep(0.8)

        return f'Message sent successfully {times} time{"s" if times > 1 else ""}'

    def many_messages(self, messages_list):
        if not messages_list:
            return 'Pass a list of messages'
        for message in messages_list:
            self.inp.send_keys(message + Keys.ENTER)
            time.sleep(0.8)

        return f'{len(messages_list)} messages sent successfully'

    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    import atexit

    phone = input('Insert the phone number with the county code: ')
    w = WhatsappAutomation(phone)
    atexit.register(w.quit)

    message = input('Insert the message you want to send: ')
    print('\n' + w.one_message(message))