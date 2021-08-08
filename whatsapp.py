from selenium import webdriver
import time
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
        self.driver.get('https://web.whatsapp.com/send?phone=+34674305378')

    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    import atexit

    phone = input('Insert the phone number with the county code: ')
    w = WhatsappAutomation(phone)

    atexit.register(w.quit)