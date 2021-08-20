# web-messages-automation
Using this project you are able to automate WhatsApp and Telegram using their web services.

## Installation
Run this commands:

```
git clone https://github.com/ToniIvars/web-messages-automation.git
cd web-messages-automation
pip install -r requirements.txt
```

It's recommended to have a virtual environment ([Virtualenv](https://pypi.org/project/virtualenv/) or [Venv](https://docs.python.org/3/library/venv.html), which is built-in).

## Usage
We will differenciate the usage of the WhatsApp and the Telegram parts, but they are very similar.

#### WhatsApp
```python
from whatsapp import WhatsappAutomation

w = WhatsappAutomation() # Creating an instance of the class

w.change_recipient('Any name') # Changing the recipient of the message by providing the name

print(w.send_message('Hello', times=3)) # Send a message a number of times, default is 1 time

print(w.send_messages(['Hi', 'How', 'Are', 'You'])) # Send 2 or more messages consecutively

w.quit() # You have to quit the driver after you have finished the automation
```


#### Telegram
```python
from telegram import TelegramAutomation

t = TelegramAutomation('666666666') # Creating an instance of the class, passing your phone number as a string parameter

t.change_recipient('Any name') # Changing the recipient of the message by providing the name

print(t.send_message('Hello', times=3)) # Send a message a number of times, default is 1 time

print(t.send_messages(['Hi', 'How', 'Are', 'You'])) # Send 2 or more messages consecutively

t.quit() # You have to quit the driver after you have finished the automation
```