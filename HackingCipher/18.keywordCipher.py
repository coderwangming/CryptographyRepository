# Simple Substitution Cipher
# http://inventwithpython.com/hacking (BSD Licensed)
#

from lib import pyperclip
import sys, random


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    myMessage = 'Help i am lost'
    keyword = 'pacific'
    print ("关键词是:",keyword)
    myMode = 'encrypt' # set to 'encrypt' or 'decrypt'
    beginLetter = 'k'
    myKey = getKey(keyword,beginLetter)
    
    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)
    print('Using key %s' % (myKey))
    print('The %sed message is:' % (myMode))
    print(translated)
    pyperclip.copy(translated)
    print()
    print('This message has been copied to the clipboard.')

def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def translateMessage(key, message, mode):
    translated = ''
    charsA = LETTERS
    charsB = key
    if mode == 'decrypt':
        # For decrypting, we can use the same code as encrypting. We
        # just need to swap where the key and LETTERS strings are used.
        charsA, charsB = charsB, charsA

    # loop through each symbol in the message
    for symbol in message:
        if symbol.upper() in charsA:
            # encrypt/decrypt the symbol
            symIndex = charsA.find(symbol.upper())
            if symbol.isupper():
                translated += charsB[symIndex].upper()
            else:
                translated += charsB[symIndex].lower()
        else:
            # symbol is not in LETTERS, just add it
            translated += symbol

    return translated
#得到密钥
# keyword 关键词
#beginLetter 开始的字母
def getKey(keyword,beginLetter):
    L = list(keyword.upper())
    beginIndex = LETTERS.find(beginLetter.upper())
    keys = ['']*len(LETTERS)
    for i in L:
        if not i in keys:
            keys[beginIndex] = i
            beginIndex = (beginIndex+1)%len(LETTERS)

    for letter in LETTERS:
        if not letter in keys:
            keys[beginIndex] = letter
            beginIndex = (beginIndex+1)%len(LETTERS)
    return "".join(keys)
    
if __name__ == '__main__':
    main()