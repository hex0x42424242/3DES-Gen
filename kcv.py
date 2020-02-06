#!/usr/bin/python3
#Renato Hormazabal

import binascii
import hashlib
import base64
import urllib.request
import requests
import re
import os
import pandas
import requests
from bs4 import BeautifulSoup
from time import sleep
from pyDes import *

os.urandom(24)    # 24*8=192 bits
os.urandom(24).hex()
key = os.urandom(24).hex()
print('Key: ' + str.upper(key))

os.urandom(24)    # 24*8=192 bits
os.urandom(24).hex()
key2 = os.urandom(24).hex()
print('Key2: ' + str.upper(key2))

os.urandom(24)    # 24*8=192 bits
os.urandom(24).hex()
key3 = os.urandom(24).hex()
print('Key3: ' + str.upper(key3))

one = key
two = key2
three = key3

r = requests.get("https://emvlab.org/keyshares/?combined=&combined_kcv=&one={one}&one_kcv=&two={two}&two_kcv=&three={three}&three_kcv=&numcomp=three&parity=ignore&action=Combine".format(one=one, two=two, three=three))

if r.status_code == 200:
    print('Requisição bem sucedida!')
    content = r.content
    #print(content)
    soup = BeautifulSoup(content, 'html.parser')
    combined_key = soup.find(id='combined').getText()
    print('Combined Key: ' + str.upper(combined_key))
print('.........................................................')

value = '000000000000000000000000000000'
key = binascii.unhexlify(key)
key2 = binascii.unhexlify(key2)
key3 = binascii.unhexlify(key3)
combined_key = binascii.unhexlify(combined_key)

print('Componet 1: ' + str(key))
print('Component 2: ' + str(key2))
print('Component 3: ' + str(key3))
print('Combined Key: ' + str(combined_key))
print('................................................')

k = triple_des(key, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
k2 = triple_des(key2, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
k3 = triple_des(key3, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
combined = triple_des(combined_key, ECB, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
data = k.encrypt(value)
data2 = k2.encrypt(value)
data3 = k3.encrypt(value)
data4 = combined.encrypt(value)

loading = 'Calculando KCV, aguarde...'
sleep(0.6)
print('KCV: Component 1: ' + str(binascii.hexlify(data)[0:6]))
sleep(0.1)
print('KCV2: Component 2: ' + str(binascii.hexlify(data2)[0:6]))
sleep(0.1)
print('KCV3: Component 3: ' + str(binascii.hexlify(data3)[0:6]))
sleep(0.1)
print('KCV Combined Key: ' + str(binascii.hexlify(data4)[0:6]))
