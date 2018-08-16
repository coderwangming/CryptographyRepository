# Caesar Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

from lib import pyperclip
import re
import sys
#message里面存储明文或者密文
# the string to be encrypted/decrypted
message = 'HOW ARE YOU'
message = 'UQXTQUYFR'
#密钥 一次性板
# the encryption/decryption key
key='NCBTZQARX'

#需要加密还是解密
# tells the program to encrypt or decrypt
mode = 'encrypt'  # set to 'encrypt' or 'decrypt'
mode = 'decrypt'
# every possible symbol that can be encrypted
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# stores the encrypted/decrypted form of the message
translated = ''

# capitalize the string in message
message = message.upper()
message = re.sub('[^A-Z]','',message)
if(len(message)!=len(key)):
    print ("ERROR,一次性版的长度应该和明文的长度一致")
    sys.exit()
# run the encryption/decryption code on each symbol in the message string
for i in range(0,len(message)):
    symbol1 = message[i]
    symbol2 = key[i]
    if symbol1 in LETTERS:
        # get the encrypted (or decrypted) number for this symbol
        num1 = LETTERS.find(symbol1)  # get the number of the symbol
        num2 = LETTERS.find(symbol2)
        if mode == 'encrypt':
            num = num1 + num2
        elif mode == 'decrypt':
            num = num1 - num2

        # handle the wrap-around if num is larger than the length of
        # LETTERS or less than 0
        if num >= len(LETTERS):
            num = num - len(LETTERS)
        elif num < 0:
            num = num + len(LETTERS)

        # add encrypted/decrypted number's symbol at the end of translated
        translated = translated + LETTERS[num]

    else:
        # just add the symbol without encrypting/decrypting
        translated = translated + symbol1

# print the encrypted/decrypted string to the screen
print(translated)

# copy the encrypted/decrypted string to the clipboard
pyperclip.copy(translated)
