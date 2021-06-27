# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import prompt
from examples import custom_style_3
from pyfiglet import Figlet
import os
import xmlrpc.client as xmlrpclib


f = Figlet(font='lean')
s = xmlrpclib.ServerProxy('http://26.53.0.146:32621')


def print_header():
    print(f.renderText('KOREAN MUSIC AWARDS'))
    print('==================================\n')

menus1 = [
    {
        'type': 'list',
        'name': 'menus1',
        'message': 'Welcome To Korean Music Awards',
        'choices': ['Generate Kode Voting', 'Melihat Kode Vote' ,'Lihat Hasil Voting' ,'Umumkan Pemenang','Keluar'],
        'filter': lambda val: val.lower()
    }
]




generate_kode = [
    {
        'type': 'confirm',
        'message': 'Apakah Kode Sudah Di-Copy ?',
        'name': 'kirim',
        'default': True,
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


def menu1():
    os.system('cls')
    print_header()
    answer = prompt(menus1, style=custom_style_3)

    return answer['menus1']

def generate_kode_voting():
    os.system('cls')
    print_header()
    kode = s.generate_code()
    print('Kode Voting : ', kode)
    prompt(generate_kode, style=custom_style_3)

def lihat_kode_voting():
    os.system('cls')
    print_header()
    kodes = s.get_code()
    for kode in kodes:
        print('Kode : ',*kode.keys())
        print('Sudah Digunakan : ',*kode.values())
    prompt(confirmation, style=custom_style_3)

def publish_pemenang():
    os.system('cls')
    print_header()
    a = s.publish_pemenang()
    print(a)
    print('PEMENANG SUDAH DIUMUMKAN')
    prompt(confirmation, style=custom_style_3)

def hasil_voting():
    os.system('cls')
    print_header()
    result = s.querry_result()
    print(result)
    prompt(confirmation, style=custom_style_3)

def main():
    os.system('cls')
    exit_menu = False
    while exit_menu == False:
        answer = menu1()
        if answer == 'generate kode voting':
            generate_kode_voting()
        if answer == 'melihat kode vote':
            lihat_kode_voting()
        if answer == 'lihat hasil voting':
            hasil_voting()
        if answer == 'umumkan pemenang':
            publish_pemenang()
        if answer == 'keluar':
            exit_menu = True

if __name__ == '__main__':
    main()