# Reverse Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

message = 'Three can keep a secret, if two of them are dead.'
message = input('输入要加密的明文:')
translated = ''

print("明文是:"+message)

i = len(message) - 1
while i >= 0:
    translated = translated + message[i]
    i = i - 1

print("结果反转加密的密文:"+translated)
message = ""
i = len(translated) - 1
while i >= 0:
    message= message + translated[i]
    i = i - 1

print("解密之后的密文:"+message)