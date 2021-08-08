from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import phonenumbers

class InvalidPhoneError(Exception):
    def __init__(self):
        self.message = 'The phone number is invalid'
        super().__init__(self.message)

class WhatsappAutomation:
    def __init__(self, phone):
        try:
            parsed_phone = phonenumbers.parse(phone, None)
        except:
            raise InvalidPhoneError

        self.driver = webdriver.Firefox()
        self.driver.get(f'https://web.whatsapp.com/send?phone={phone}')

        print('Read the QR code with your phone, please (this will only occur once).')

        WebDriverWait(self.driver, 20).until(lambda s:s.find_element_by_id('side'))
        self.driver.minimize_window()

    def one_message(self, message, times=1):
        inp = WebDriverWait(self.driver, 10).until(lambda s:s.find_element_by_css_selector('._1LbR4 > div:nth-child(2)'))
        for _ in range(times):
            inp.send_keys(message + Keys.ENTER)

    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    import atexit

    phone = input('Insert the phone number with the county code: ')
    w = WhatsappAutomation(phone)

    atexit.register(w.quit)