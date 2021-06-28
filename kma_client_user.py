from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import prompt
from examples import custom_style_3
from pyfiglet import Figlet
import os
import xmlrpc.client as xmlrpclib
# import paho mqtt
import paho.mqtt.client as mqtt
import uuid

f = Figlet(font='lean')
s = xmlrpclib.ServerProxy('http://26.53.0.146:32621')


def print_header():
    print(f.renderText('KOREAN MUSIC AWARDS'))
    print('==================================\n')

menuUtama = [
    {
        'type': 'list',
        'name': 'menuUtama',
        'message': 'Welcome To Korean Music Awards Voting',
        'choices': ['Voting', 'Hasil Voting','Keluar'],
        'filter': lambda val: val.lower()
    }
]

confirmation = [
    {
        'type': 'confirm',
        'message': 'Confirm?',
        'name': 'kirim',
        'default': True,
    }
]

input_voting = [
    {
        'type': 'input',
        'name': 'candidate',
        'message': 'Silahkan input yang anda vote',
    }
]


def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

def menu1():
    os.system('cls')
    print_header()
    answer = prompt(menuUtama, style=custom_style_3)

    return answer['menuUtama']

def voting(code):
    os.system('cls')
    print_header()
    candidates = s.get_candidate()
    print('LIST BOY/GIRL GROUP')
    for candidate in candidates:
        print(candidate)
    
    vote =  prompt(input_voting, style=custom_style_3)
    message = s.vote(code, vote['candidate'])
    print(message)
    prompt(confirmation, style=custom_style_3)

broker_address = "test.mosquitto.org"
def hasil():
    os.system('cls')
    print_header()
    exit_menu = False
    client = mqtt.Client(str(uuid.uuid1()))
    client.on_message = on_message
    client.connect(broker_address, port=1883)
    client.loop_start()
    while exit_menu == False:
        print("MENUNGGU HASIL VOTING")
        client.subscribe("KMA_WINNER")
        answer = prompt(confirmation, style=custom_style_3)
        if(answer['kirim'] == True):
            exit_menu = True
    client.disconnect()
    client.loop_stop()

def main():
    os.system('cls')
    exit_menu = False
    while exit_menu == False:
        answer = menu1()
        if answer == 'keluar':
            exit_menu = True
        if answer == 'voting':
            code = input("INPUT KODE VOTING : ")
            valid = s.check_code(code)
            if valid == True:
                voting(code)
            else:
                print('Kode Tidak Valid')
                prompt(confirmation, style=custom_style_3)
        if answer == 'hasil voting':
            hasil()


if __name__ == '__main__':
    main()