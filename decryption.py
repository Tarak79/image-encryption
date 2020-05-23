
import random
import gzip
import cv2
import matplotlib.pyplot as plt

digits = 3
import numpy as np

def dec(col, key,n):
    return chr((col ** key) % n)

def split_string(string,digits):
    return [string[start:start+digits] for start in range(0, len(string), digits)]

def decode_image(dec):
    height1 = int(dec[-4:])
    width1 = int(dec[-8:-4])

    flatten_array = np.array(list(map(int, split_string(dec[:-8],3))))
    return flatten_array.reshape(width1,height1,3)

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    ciphertext  = gzip.decompress(ciphertext).decode("utf-8")
    digits = 3
    key, n = pk
    arr = split_string(ciphertext, digits)
    
    plain = []
    for i in arr:
        plain.append(dec(int(i),key,n))

    #Return the array of bytes as a string
    return ''.join(map(lambda x: str(x), plain))

private = input("please enter private key: ")
private = (int(private[:5]), int(private[5:10]))
print(private)

with open("encrypted_file.txt",'rb') as f:
    encrypted_msg = f.read()


print("Decrypting message with private key . . .")
decrypted_msg = decrypt(private, encrypted_msg)
#print("Decrypted message: ",decrypted_msg)


req_img = decode_image(decrypted_msg)
cv2.imwrite("decrypted_image.png", req_img)
print(np.shape(req_img))
plt.imshow(req_img)
plt.show()

