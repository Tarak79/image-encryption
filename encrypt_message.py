import cv2
import pandas as pd
import random
import numpy as np
import gzip
from key_pair_generation import generate_keypair


def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in range(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

primes = [i for i in range(1,20) if is_prime(i)]


def encode_image(path):
    im = cv2.imread(path)
    arr = im.reshape(-1)

    width = im.shape[0]
    height = im.shape[1]
    plaintextstr = ''
    for i in arr:
        plaintextstr += format(i,"03d" )
    return plaintextstr + format(width, "04d") + format(height, "04d")

def enc(col, pk, n):
    return (ord(col) ** pk) % n

def encrypt(pk, plaintext):
    digits = 3
    #Unpack the key into it's components
    key, n = pk
    
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = []
    for i in plaintext:
        cipher.append(enc(i,key,n))
    print("max value in cipher: ",max(cipher))

    #Return the array of bytes
    plain = []
    
    for i in cipher:
        plain.append(format(i, '0{}d'.format(digits)))
    encrypted_msg = ''.join(map(lambda x: str(x), plain))
    compressed_value = gzip.compress(bytes(encrypted_msg,'utf-8'))
    return compressed_value

if __name__ == '__main__':
    '''
    Detect if the script is being run directly by the user
    '''
    image_path = "cap.jpg"
    msg = encode_image(image_path)
    #msg = input("Enter a message to encrypt with your private key: ")

    print("RSA Encrypter/ Decrypter")

    p = int(random.choice(primes))
    q = int(random.choice(np.delete(primes, primes.index(p))))

    print("primes :",p,' ',q)
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    i,j = private
    print("Your public key is ", public ," and your private key is ", format(i, "05d")+format(j, "05d"))
    
    encrypted_msg = encrypt(public, msg)

    with open("encrypted_file.txt",'wb') as f:
    	f.write(encrypted_msg)
