# RSA Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import sys

# 默认的加密块的长度 128B=1024bits
# IMPORTANT: The block size MUST be less than or equal to the key size!
# (Note: The block size is in bytes, the key size is in bits. There
# are 8 bits in 1 byte.)
DEFAULT_BLOCK_SIZE = 128  # 128 bytes
# 2的8次方 等于256，一个字节可以有256个值
BYTE_SIZE = 256  # One byte has 256 different values.


def main():

    # Runs a test that encrypts a message to a file or decrypts a message
    # from a file.
    #将密文写到这个文件中/从这个文件中读取密文
    filename = 'files/encrypted_file.txt'  # the file to write to/read from
    mode = 'encrypt'  # set to 'encrypt' or 'decrypt'

    if mode == 'encrypt':
        message = '''"Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets." -Gerald Priestland "The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people." -Hugo Black'''
        pubKeyFilename = 'al_sweigart_pubkey.txt'
        print('Encrypting and writing to %s...' % (filename))
        encryptedText = encryptAndWriteToFile(filename, pubKeyFilename, message)

        print('Encrypted text:')
        print(encryptedText)

    elif mode == 'decrypt':
        privKeyFilename = 'al_sweigart_privkey.txt'
        print('Reading from %s and decrypting...' % (filename))
        decryptedText = readFromFileAndDecrypt(filename, privKeyFilename)

        print('Decrypted text:')
        print(decryptedText)

'''
    比如要计算 42! 的块，按照以下的步骤，其中的256代表BYTE_SIZE
    序号  字母  ascii   blockInt
    0       4   52      52*（256^0）=52
    1       2   50      50*(256^1)=12800
    2       !   33      33*(256^2)=2162688
    最后:blockInt = 52 + 12800 + 2162688 = 2175540
'''
# 将明文切分成块
# 输入 message：明文
#   blockSize：加密快的大小
#输出：明文计算出的块的list，list中的每一个值代表明文中一个块计算出的int值
def getBlocksFromText(message, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts a string message to a list of block integers. Each integer
    # represents 128 (or whatever blockSize is set to) string characters.

    messageBytes = message.encode('ascii')  # convert the string to bytes

    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        #blockInt代表一个块计算出来的int
        # Calculate the block integer for this block of text
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts

#将块转化为文本
#输入：blockInts:块的list
#   messageLength:文本的长度
#   blockSize:块大小
def getTextFromBlocks(blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts a list of block integers to the original message string.
    # The original message length is needed to properly convert the last
    # block integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize - 1, -1, -1):
            if len(message) + i < messageLength:
                # Decode the message string for the 128 (or whatever
                # blockSize is set to) characters from this block integer.
                asciiNumber = blockInt // (BYTE_SIZE ** i)
                blockInt = blockInt % (BYTE_SIZE ** i)
                blockMessage.insert(0, chr(asciiNumber))
        message.extend(blockMessage)
    return ''.join(message)


# 加密信息
# 输入 message：要加密的明文
#    key：公钥（n,e）
#    blockSize：加密块的长度
def encryptMessage(message, key, blockSize=DEFAULT_BLOCK_SIZE):
    # Converts the message string into a list of block integers, and then
    # encrypts each block integer. Pass the PUBLIC key to encrypt.
    encryptedBlocks = []
    n, e = key

    for block in getBlocksFromText(message, blockSize):
        # ciphertext = plaintext ^ e mod n
        #pow(a,b,c)的含义是a^b%c
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks

#解密信息
#输入 encryptedBlocks:加密的块，是一个由大整数构成的list
#   messageLength:密文的长度
#   key:密钥（n,d）
#   blockSize:块的大小
def decryptMessage(encryptedBlocks, messageLength, key, blockSize=DEFAULT_BLOCK_SIZE):
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength, blockSize)


# 从文件中读取key
# 输入：存放key的文件路径
# 输出：key的长度（单位：bits） n e或d
def readKeyFile(keyFilename):
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n,e) or (n,d) tuple value.
    fo = open(keyFilename)
    content = fo.read()
    fo.close()
    keySize, n, EorD = content.split(',')
    return (int(keySize), int(n), int(EorD))

#加密信息并且将密文写入文件
#输入：  messageFilename:将密文写入到这个文件中
#       keyFilename:公钥所在的位置
#       message:明文
#       blockSize:块的大小 单位:B
#输出:  明文的长度_块大小_加密之后的密文
def encryptAndWriteToFile(messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    keySize, n, e = readKeyFile(keyFilename)

    # key的长度应该大于等于加密块的长度
    # Check that key size is greater than block size.
    if keySize < blockSize * 8:  # * 8 to convert bytes to bits
        sys.exit(
            'ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (
            blockSize * 8, keySize))

    # Encrypt the message
    encryptedBlocks = encryptMessage(message, (n, e), blockSize)

    # Convert the large int values to one string value.
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    # Write out the encrypted string to the output file.
    encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)
    fo = open(messageFilename, 'w')
    fo.write(encryptedContent)
    fo.close()
    # Also return the encrypted string.
    return encryptedContent

#从文件中读取密文并解密
#输入：    messageFilename:存储密文的文件位置
#       keyFilename:密钥所在的文件位置
#输出：解密之后的明文
def readFromFileAndDecrypt(messageFilename, keyFilename):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    keySize, n, d = readKeyFile(keyFilename)

    # Read in the message length and the encrypted message from the file.
    fo = open(messageFilename)
    content = fo.read()
    messageLength, blockSize, encryptedMessage = content.split('_')
    messageLength = int(messageLength)
    blockSize = int(blockSize)

    # Check that key size is greater than block size.
    if keySize < blockSize * 8:  # * 8 to convert bytes to bits
        sys.exit(
            'ERROR: Block size is %s bits and key size is %s bits. The RSA cipher requires the block size to be equal to or greater than the key size. Did you specify the correct key file and encrypted file?' % (
            blockSize * 8, keySize))

    # Convert the encrypted message into large int values.
    encryptedBlocks = []
    for block in encryptedMessage.split(','):
        encryptedBlocks.append(int(block))

    # Decrypt the large int values.
    return decryptMessage(encryptedBlocks, messageLength, (n, d), blockSize)


# If rsaCipher.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()
