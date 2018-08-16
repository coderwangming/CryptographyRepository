# Caesar Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

from lib import pyperclip

#message里面存储明文或者密文
# the string to be encrypted/decrypted
message = 'This is my secret message.'
message = "'You can show black is white by argument,' said Filby, 'but you will never convince me.'"
message = "1234567890"
message = "'Kv uqwpfu rncwukdng gpqwij.'"
message = "Xqp whh ahoa kb pda sknhz swo ejreoexha."

#密钥
# the encryption/decryption key
key = 13
key = 8
key = 21
key = 2
key = 22

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

# run the encryption/decryption code on each symbol in the message string
for symbol in message:
    if symbol in LETTERS:
        # get the encrypted (or decrypted) number for this symbol
        num = LETTERS.find(symbol)  # get the number of the symbol
        if mode == 'encrypt':
            num = num + key
        elif mode == 'decrypt':
            num = num - key

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
        translated = translated + symbol

# print the encrypted/decrypted string to the screen
print(translated)

# copy the encrypted/decrypted string to the clipboard
pyperclip.copy(translated)
