#!/usr/bin/python3

import binascii
import os
from pyDes import *

def calculate_combined_key(keys):
    return "".join([
        hex(int(ck1,16) ^ int(ck2,16) ^ int(ck3,16)).split('x')[1].upper() 
        for ck1,ck2,ck3 in zip(keys[0],keys[1],keys[2])
    ])

def generate_keys():
    return tuple([os.urandom(24).hex().upper() for _ in range(3)])

def generate_kcv(key):

    validation_data = binascii.unhexlify('0' * 30)
    
    tdes_obj = triple_des(binascii.unhexlify(key),ECB,"\0\0\0\0\0\0\0\0",pad=None,padmode=PAD_PKCS5)

    return binascii.hexlify(tdes_obj.encrypt(validation_data)).decode('utf-8')

if __name__ == '__main__':
    # Gera as 3 chaves de 56 bits
    keys = generate_keys()

    # Gera combined key
    combined_key = calculate_combined_key(keys)

    for i,k in enumerate(keys):
        print(f"Key {i}:        {k}    KCV: {generate_kcv(k)}")

    print(f"Combined Key: {combined_key}    KCV: {generate_kcv(combined_key)}")
